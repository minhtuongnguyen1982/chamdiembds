import re

def analyze_and_score_lead(description: str):
    """
    Hàm chấm điểm Lead Bất Động Sản dựa trên bộ quy tắc nghiệp vụ.
    
    Quy tắc:
    - Base Score: 50 điểm.
    - +50 điểm cho các tiêu chí VIP / Siêu tiềm năng (Ngân sách >= 20 tỷ / tài chính mạnh, Loại hình cao cấp, Vị trí đắc địa, Đối tượng VIP, Cấp thiết & Minh bạch).
    - -50 điểm cho các dấu hiệu Rác / Không tiềm năng (Yêu cầu phi thực tế, Không nhu cầu, Không thiện chí, Spam, Lỗi liên lạc).
    - +0..+10 cho các nhu cầu thực phân khúc tầm trung.
    """
    if not isinstance(description, str) or not description.strip():
        return {
            "ai_score": 0,
            "ai_tier": "Không tiềm năng / Rác",
            "plus_reasons": [],
            "minus_reasons": [],
            "neutral_reasons": ["Không có thông tin mô tả nhu cầu."],
            "matched_keywords": [],
            "ai_summary": "⚠️ Không có mô tả nhu cầu khách hàng."
        }

    text_lower = description.lower()
    
    base_score = 50
    plus_reasons = []
    minus_reasons = []
    neutral_reasons = []
    matched_keywords = []

    # -------------------------------------------------------------
    # 1. TIÊU CHÍ CỘNG 50 ĐIỂM (KHÁCH HÀNG VIP / SIÊU TIỀM NĂNG)
    # -------------------------------------------------------------
    
    # 1.1 Ngân sách lớn (>= 20 tỷ hoặc từ khóa tài chính mạnh)
    has_big_budget = False
    
    # Check regex for numbers >= 20 tỷ
    budget_matches = re.findall(r'(\d+)\s*(tỷ|ty|tỉ)', text_lower)
    for num_str, _ in budget_matches:
        try:
            val = float(num_str)
            if val >= 20:
                has_big_budget = True
                plus_reasons.append(f"Ngân sách lớn ({val:g} tỷ >= 20 tỷ)")
                matched_keywords.append(f"{val:g} tỷ")
        except ValueError:
            pass

    # Check phrases for strong finance / no problem budget
    strong_finance_keywords = [
        "tài chính mạnh", "tài chính cực mạnh", "tài chính khủng", 
        "ngân sách không thành vấn đề", "không thành vấn đề", "tài chính không thành vấn đề"
    ]
    for kw in strong_finance_keywords:
        if kw in text_lower:
            if not has_big_budget:
                plus_reasons.append(f"Tài chính cực mạnh ({kw})")
                has_big_budget = True
            matched_keywords.append(kw)

    # 1.2 Loại hình cao cấp
    premium_property_keywords = {
        "biệt thự đơn lập": "Biệt thự đơn lập",
        "penthouse": "Penthouse",
        "shophouse mặt đường lớn": "Shophouse mặt đường lớn",
        "quỹ đất công nghiệp": "Quỹ đất công nghiệp",
        "đất công nghiệp": "Quỹ đất công nghiệp",
        "sàn văn phòng diện tích lớn": "Sàn văn phòng diện tích lớn",
        "sàn văn phòng": "Sàn văn phòng diện tích lớn"
    }
    for kw, label in premium_property_keywords.items():
        if kw in text_lower and not any(label in r for r in plus_reasons):
            plus_reasons.append(f"Loại hình cao cấp ({label})")
            matched_keywords.append(kw)

    # 1.3 Vị trí đắc địa
    prime_location_keywords = {
        "quận 1": "Vị trí Quận 1",
        "q1": "Vị trí Quận 1",
        "q.1": "Vị trí Quận 1",
        "ven sông": "BĐS ven sông",
        "vinhomes ocean park": "Vinhomes Ocean Park",
        "phú mỹ hưng": "Phú Mỹ Hưng"
    }
    # Note: avoid matching Q1 if it's junk context like "mua nhà Q1 giá 1 tỷ"
    is_q1_junk = "đòi mua nhà q1" in text_lower or "nhà q1 giá 1 tỷ" in text_lower or "quận 1 giá 1 tỷ" in text_lower
    for kw, label in prime_location_keywords.items():
        if kw in text_lower and not is_q1_junk and not any(label in r for r in plus_reasons):
            plus_reasons.append(f"Vị trí đắc địa ({label})")
            matched_keywords.append(kw)

    # 1.4 Đối tượng khách hàng VIP
    vip_target_keywords = {
        "chủ doanh nghiệp": "Chủ doanh nghiệp lớn",
        "nhà đầu tư chuyên nghiệp": "Nhà đầu tư chuyên nghiệp",
        "mua sỉ": "Mua sỉ BĐS",
        "mua số lượng lớn": "Mua số lượng lớn"
    }
    for kw, label in vip_target_keywords.items():
        if kw in text_lower and not any(label in r for r in plus_reasons):
            plus_reasons.append(f"Đối tượng VIP ({label})")
            matched_keywords.append(kw)

    # 1.5 Tính cấp thiết & Minh bạch
    transparency_keywords = {
        "pháp lý chuẩn 100%": "Pháp lý chuẩn 100%",
        "pháp lý chuẩn": "Pháp lý chuẩn",
        "sổ hồng riêng": "Sổ hồng riêng",
        "gặp trực tiếp chủ đầu tư": "Cần gặp trực tiếp CĐT đàm phán",
        "gặp trực tiếp chủ": "Cần gặp trực tiếp CĐT đàm phán"
    }
    for kw, label in transparency_keywords.items():
        if kw in text_lower and not any(label in r for r in plus_reasons):
            plus_reasons.append(f"Minh bạch & Cấp thiết ({label})")
            matched_keywords.append(kw)

    # -------------------------------------------------------------
    # 2. TIÊU CHÍ TRỪ 50 ĐIỂM (KHÁCH HÀNG RÁC / KHÔNG TIỀM NĂNG)
    # -------------------------------------------------------------

    # 2.1 Yêu cầu phi thực tế
    unrealistic_keywords = [
        "phi thực tế", "rất thấp so với mặt bằng chung", "đòi mua nhà q1", "đòi mua nhà quận 1",
        "nhà q1 giá 1 tỷ", "quận 1 giá 1 tỷ", "giá 2 triệu ở trung tâm", "vài trăm triệu"
    ]
    for kw in unrealistic_keywords:
        if kw in text_lower:
            minus_reasons.append("Yêu cầu phi thực tế / Ngân sách bất khả thi")
            matched_keywords.append(kw)
            break

    # 2.2 Không có nhu cầu
    no_need_keywords = {
        "nhầm số": "Khách nhầm số",
        "không có nhu cầu": "Không có nhu cầu BĐS",
        "dữ liệu cũ": "Dữ liệu cũ / Trộn ngành khác",
        "nhầm ngành": "Dữ liệu nhầm ngành"
    }
    for kw, label in no_need_keywords.items():
        if kw in text_lower and not any(label in r for r in minus_reasons):
            minus_reasons.append(f"Không có nhu cầu ({label})")
            matched_keywords.append(kw)

    # 2.3 Khách hàng không thiện chí
    uncooperative_keywords = {
        "hỏi giá cho vui": "Hỏi giá cho vui",
        "chưa có ý định mua": "Chưa có ý định mua",
        "thái độ không hợp tác": "Thái độ không hợp tác"
    }
    for kw, label in uncooperative_keywords.items():
        if kw in text_lower and not any(label in r for r in minus_reasons):
            minus_reasons.append(f"Không thiện chí ({label})")
            matched_keywords.append(kw)

    # 2.4 Spam / Quảng cáo
    spam_keywords = {
        "bảo hiểm": "Spam / Mời bảo hiểm",
        "vay vốn": "Spam / Mời vay vốn",
        "mời chào dịch vụ": "Spam / Quảng cáo dịch vụ",
        "dịch vụ khác": "Spam / Quảng cáo"
    }
    for kw, label in spam_keywords.items():
        if kw in text_lower and not any(label in r for r in minus_reasons):
            minus_reasons.append(f"Quảng cáo / Spam ({label})")
            matched_keywords.append(kw)

    # 2.5 Thông tin liên lạc lỗi
    contact_error_keywords = {
        "thuê bao": "SĐT bị thuê bao",
        "gọi nhiều lần không bắt máy": "Gọi nhiều lần không nghe máy",
        "không bắt máy": "Không bắt máy",
        "không phản hồi zalo": "Không phản hồi Zalo"
    }
    for kw, label in contact_error_keywords.items():
        if kw in text_lower and not any(label in r for r in minus_reasons):
            minus_reasons.append(f"Lỗi liên lạc ({label})")
            matched_keywords.append(kw)

    # -------------------------------------------------------------
    # 3. TRƯỜNG HỢP KHÁC (TRUNG TÍNH / THỰC TẾ TẦM TRUNG)
    # -------------------------------------------------------------
    mid_tier_keywords = {
        "căn hộ 2pn": "Căn hộ 2PN tầm trung",
        "quận 7": "Khu vực Quận 7",
        "nhà phố liền kề": "Nhà phố liền kề tầm trung",
        "đất nền vùng ven": "Đất nền vùng ven (Long An, Đồng Nai)",
        "long an": "Khu vực Long An",
        "đồng nai": "Khu vực Đồng Nai",
        "vay ngân hàng": "Nhu cầu hỗ trợ vay ngân hàng",
        "chính sách chiết khấu": "Quan tâm chính sách chiết khấu",
        "cần tư vấn thêm": "Cần tư vấn thêm thông tin"
    }
    has_mid_tier = False
    for kw, label in mid_tier_keywords.items():
        if kw in text_lower and not any(label in r for r in neutral_reasons):
            neutral_reasons.append(f"Phân khúc tầm trung ({label})")
            has_mid_tier = True
            matched_keywords.append(kw)

    # -------------------------------------------------------------
    # 4. TÍNH TOÁN ĐIỂM SỐ VÀ PHÂN LOẠI TẦNG KHÁCH HÀNG
    # -------------------------------------------------------------
    score_change = (len(plus_reasons) * 50) - (len(minus_reasons) * 50)
    
    if len(plus_reasons) == 0 and len(minus_reasons) == 0:
        if has_mid_tier:
            score_change += 10 # Cộng 10 điểm thưởng cho nhu cầu thực tầm trung

    final_score = base_score + score_change
    
    # Clamp score to range [0, 100]
    final_score = max(0, min(100, final_score))

    # Determine Tier
    if final_score >= 80:
        ai_tier = "VIP / Siêu tiềm năng"
        summary_prefix = "🌟 KHÁCH HÀNG VIP / SIÊU TIỀM NĂNG"
    elif final_score >= 40:
        ai_tier = "Tiềm năng"
        summary_prefix = "✅ KHÁCH HÀNG TIỀM NĂNG"
    else:
        ai_tier = "Không tiềm năng / Rác"
        summary_prefix = "⛔ KHÁCH HÀNG RÁC / KHÔNG TIỀM NĂNG"

    # Format AI Summary string
    reasons_list = []
    if plus_reasons:
        reasons_list.append("Cộng điểm: " + ", ".join(plus_reasons))
    if minus_reasons:
        reasons_list.append("Trừ điểm: " + ", ".join(minus_reasons))
    if neutral_reasons and not plus_reasons and not minus_reasons:
        reasons_list.append("Ghi nhận: " + ", ".join(neutral_reasons))

    ai_summary = f"{summary_prefix} ({final_score} điểm). " + (" | ".join(reasons_list) if reasons_list else "Đủ điều kiện tiêu chuẩn.")

    # Deduplicate matched keywords
    matched_keywords = sorted(list(set(matched_keywords)))

    return {
        "ai_score": final_score,
        "ai_tier": ai_tier,
        "plus_reasons": plus_reasons,
        "minus_reasons": minus_reasons,
        "neutral_reasons": neutral_reasons,
        "matched_keywords": matched_keywords,
        "ai_summary": ai_summary
    }

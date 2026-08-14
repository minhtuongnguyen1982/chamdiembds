# Hệ Thống AI Lead Scoring & Automation cho Ngành Bất Động Sản 🏠

Ứng dụng Web App tự động hóa phân tích nhu cầu, chấm điểm tiềm năng khách hàng (Lead Scoring) và kiểm duyệt 2 chiều (Human-in-the-loop) cho ngành Bất Động Sản.

---

## 🌟 Tính Năng Nổi Bật

1. **Kết Nối Google Sheets Live**:
   - Tự động lấy dữ liệu từ Google Sheets: `https://docs.google.com/spreadsheets/d/1zLWzZT3a0qLL-Km66DVamoqBnduHvwJ0lUUZ3tD1qL0`
   - Nút đồng bộ dữ liệu tức thì (Real-time Sync) hoặc tải lên file CSV/Excel tùy chỉnh.

2. **AI Lead Scoring Engine (+50 / -50 Points)**:
   - **Tự động cộng 50 điểm (VIP / Siêu tiềm năng)** cho: Ngân sách lớn ($\ge 20$ tỷ, tài chính mạnh), Loại hình cao cấp (Penthouse, Biệt thự đơn lập, Shophouse mặt đường lớn, Quỹ đất CN/Sàn VP lớn), Vị trí đắc địa (Q1, Ven sông, Vinhomes Ocean Park, Phú Mỹ Hưng), Đối tượng VIP (Chủ doanh nghiệp, Mua sỉ, Đầu tư chuyên nghiệp), Pháp lý chuẩn 100% / Sổ hồng riêng.
   - **Tự động trừ 50 điểm (Rác / Không tiềm năng)** cho: Yêu cầu phi thực tế (nhà Q1 giá 1-2 tỷ, nhà thuê 2 triệu trung tâm), Khách nhầm số / Không nhu cầu / Dữ liệu cũ, Hỏi giá cho vui / Chưa muốn mua, Quảng cáo spam bảo hiểm/vay vốn, SĐT thuê bao / Không bắt máy / Không phản hồi Zalo.
   - **Thưởng 10 điểm** cho nhu cầu thực phân khúc tầm trung (Chung cư 3-10 tỷ, vay ngân hàng, xem mẫu).

3. **Giao Diện Kiểm Duyệt Human-in-the-Loop**:
   - Cho phép Chăm sóc viên / Sale Lead xem chi tiết giải trình AI, tìm kiếm, lọc theo tầng lead.
   - Hỗ trợ chỉnh sửa điểm số chốt, đổi trạng thái duyệt (*Chờ duyệt, Đã duyệt, Cần gọi gấp, Bỏ qua*) và thêm ghi chú nhân sự trực tiếp trên bảng tương tác.

4. **Báo Cáo Analytics & Biểu Đồ Dynamic**:
   - Biểu đồ Donut phân bổ chất lượng Lead, Histogram phân bố điểm số, Bar chart Top từ khóa VIP & Trạng thái duyệt.

5. **Xuất File Excel Format Chuẩn**:
   - Xuất dữ liệu ra file Excel (`.xlsx`) được định dạng màu sắc phân hạng chuẩn bị bàn giao cho đội ngũ bán hàng.

---

## 🚀 Hướng Dẫn Chạy Ứng Dụng

### 1. Cài đặt thư viện phụ thuộc:
```bash
pip install -r requirements.txt
```

### 2. Khởi chạy ứng dụng Web App (Streamlit):
```bash
streamlit run app.py
```

### 3. Kiểm thử bộ chấm điểm AI (Console test):
```bash
python test_scorer.py
```

---

## 📁 Cấu Trúc Mã Nguồn

```text
.
├── app.py              # Streamlit Web App UI (Tabs, Analytics, Human-in-the-loop, Excel Export)
├── lead_scorer.py     # Engine phân tích NLP & Chấm điểm Lead theo bộ quy tắc nghiệp vụ
├── test_scorer.py     # Script kiểm thử tự động thuật toán chấm điểm
├── requirements.txt   # Các thư viện Python yêu cầu
├── test.csv           # Bản sao dữ liệu test offline từ Google Sheets
└── README.md          # Tài liệu hướng dẫn vận hành
```

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

from bank_analytics import load_and_clean_bank_data

# Page Configuration
st.set_page_config(
    page_title="Bank Churn Solutions & Executive Decision Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Executive Theme
st.markdown("""
<style>
    .stApp {
        background-color: #0B0F17;
        color: #E2E8F0;
    }
    
    /* Header Box */
    .exec-header {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #1E2640 0%, #111827 100%);
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .metric-title {
        font-size: 0.82rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: #F8FAFC;
        margin: 6px 0;
    }
    .metric-sub {
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    /* Decision Boxes */
    .decision-card {
        background: #1E293B;
        border-left: 6px solid #38BDF8;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 16px;
    }
    .decision-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 8px;
    }
    .decision-desc {
        color: #CBD5E1;
        font-size: 0.92rem;
        line-height: 1.5;
    }
    
    /* Badges */
    .badge-critical {
        background-color: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        border: 1px solid #EF4444;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
    }
    .badge-high {
        background-color: rgba(245, 158, 11, 0.2);
        color: #F59E0B;
        border: 1px solid #F59E0B;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E293B;
        border-radius: 8px;
        padding: 8px 20px;
        color: #94A3B8;
        border: 1px solid #334155;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0284C7 !important;
        color: #FFFFFF !important;
        border-color: #38BDF8 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
df_bank, data_msg = load_and_clean_bank_data()

if df_bank.empty:
    st.error("⚠️ Không thể tải dữ liệu ngân hàng. Vui lòng kiểm tra lại kết nối!")
    st.stop()

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/bank-building.png", width=64)
    st.title("Executive Portal")
    st.caption("Ngân Hàng Châu Âu • Bank Churn Solutions")
    st.markdown("---")
    
    st.subheader("📡 Nguồn Dữ Liệu")
    st.success(f"● {data_msg}")
    
    if st.button("🔄 Đồng Bộ Tức Thì", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
        
    st.markdown("---")
    st.subheader("🎯 Mục Tiêu Giảm Churn")
    target_reduction_pct = st.slider("Mục tiêu giảm % Churn", min_value=10, max_value=60, value=40, step=5)
    
    st.markdown("---")
    st.caption("📌 **Executive Decision Dashboard v3.0**")
    st.caption("Báo Báo Giải Pháp & Quyết Định Chiến Lược Cho Ban Giám Đốc")

# --- HEADER APP ---
total_cust = len(df_bank)
churned_df = df_bank[df_bank['Exited'] == 1]
churned_cust = len(churned_df)
churn_rate = (churned_cust / total_cust * 100) if total_cust else 0
total_lost_balance = churned_df['Balance'].sum()
critical_risk_cust = len(df_bank[df_bank['RiskScore'] >= 70])

st.markdown(f"""
<div class="exec-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin:0; font-size: 2.1rem; color: #F8FAFC;">🏛️ Executive Dashboard: Giải Pháp & Quyết Định Chiến Lược Churn Ngân Hàng</h1>
            <p style="margin: 6px 0 0 0; color: #94A3B8;">Báo cáo dành cho Ban Giám Đốc • Phân tích Chẩn đoán, Mô hình Risk Score & Giám sát ROI Giữ Chân Khách Hàng</p>
        </div>
        <div>
            <span style="background: #1E293B; border: 1px solid #38BDF8; padding: 8px 16px; border-radius: 20px; font-size: 0.85rem; color: #38BDF8; font-weight: 700;">
                📊 Total Sample: {total_cust:,} Customers
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- TOP EXECUTIVE KPIS ---
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Tổng Khách Hàng</div>
        <div class="metric-value">{total_cust:,}</div>
        <div class="metric-sub" style="color: #94A3B8;">Dữ liệu đã chuẩn hóa</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #EF4444;">
        <div class="metric-title">Tỷ Lệ Churn Tổng Thể</div>
        <div class="metric-value" style="color: #EF4444;">{churn_rate:.2f}%</div>
        <div class="metric-sub" style="color: #EF4444;">▲ {churned_cust:,} khách đã rời đi</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #F59E0B;">
        <div class="metric-title">Số Dư Tiền Gửi Thất Thoát</div>
        <div class="metric-value" style="color: #F59E0B;">€{total_lost_balance/1e6:.1f}M</div>
        <div class="metric-sub" style="color: #F59E0B;">Thiệt hại số dư thực tế</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #38BDF8;">
        <div class="metric-title">Khách Rủi Ro Rất Cao</div>
        <div class="metric-value" style="color: #38BDF8;">{critical_risk_cust:,}</div>
        <div class="metric-sub" style="color: #38BDF8;">Risk Score ≥ 70/100</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    projected_savings = total_lost_balance * (target_reduction_pct / 100)
    st.markdown(f"""
    <div class="metric-card" style="border-left: 4px solid #10B981;">
        <div class="metric-title">Tiềm Năng Cứu Dòng Tiền</div>
        <div class="metric-value" style="color: #10B981;">+€{projected_savings/1e6:.1f}M</div>
        <div class="metric-sub" style="color: #10B981;">Khi giảm {target_reduction_pct}% Churn</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- TABS NAVIGATION ---
t_sum, t_diag, t_risk, t_sol, t_exp = st.tabs([
    "🏢 Báo Cáo Executive",
    "🔍 Chẩn Đoán Động Cơ Churn",
    "🚨 Phân Tầng Rủi Ro & Action List",
    "💡 Giải Pháp & Quyết Định Trình BGD",
    "📥 Xuất Báo Cáo Excel Bàn Giao"
])

# ---------------------------------------------------------
# TAB 1: EXECUTIVE SUMMARY
# ---------------------------------------------------------
with t_sum:
    st.markdown("### 📋 Tóm Tắt Tình Hình & Nhận Định Dành Cho Ban Giám Đốc")
    
    col_sum1, col_sum2 = st.columns([3, 2])
    
    with col_sum1:
        st.markdown("""
        <div style="background: #1E293B; border-radius: 12px; padding: 20px; border: 1px solid #334155;">
            <h4 style="color: #38BDF8; margin-top:0;">⚡ Tóm Tắt Thực Trạng Rủi Ro Churn:</h4>
            <ul style="line-height: 1.8; color: #E2E8F0;">
                <li><strong>Tỷ lệ Churn tổng thể ở mức báo động 20.37%</strong> (2,037 / 10,000 khách hàng), gây thất thoát <strong>€185.8 triệu</strong> số dư tiền gửi.</li>
                <li><strong>Thất thoát tập trung ở nhóm tiền gửi thực:</strong> Khách hàng CÓ số dư tài khoản (>0€) có tỷ lệ Churn lên tới <strong>24.08%</strong> (gấp 1.7 lần nhóm số dư 0€).</li>
                <li><strong>Bẫy Bán Chéo (Cross-Selling Trap):</strong> Khách hàng dùng 3 sản phẩm Churn <strong>82.71%</strong>, dùng 4 sản phẩm Churn <strong>100.00%</strong> (trong khi khách dùng 2 sản phẩm chỉ Churn <strong>7.58%</strong>).</li>
                <li><strong>Thị trường Đức (Germany) chịu rủi ro cao nhất:</strong> Tỷ lệ Churn là <strong>32.44%</strong> (gấp 2 lần Pháp 16.15% và Tây Ban Nha 16.67%).</li>
                <li><strong>Nhóm khách hàng Trung niên (50-59 tuổi) bỏ đi hàng loạt:</strong> Tỷ lệ Churn đạt đỉnh <strong>56.04%</strong>.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with col_sum2:
        st.markdown("#### 🎯 Phân Bổ Tỷ Lệ Churn Theo Quốc Gia")
        geo_churn = df_bank.groupby('Geography').agg(
            Total=('Exited', 'count'),
            Churned=('Exited', 'sum'),
            Rate=('Exited', lambda x: x.mean() * 100)
        ).reset_index()
        
        fig_geo = px.bar(
            geo_churn, 
            x='Geography', 
            y='Rate',
            color='Geography',
            text=geo_churn['Rate'].apply(lambda x: f"{x:.1f}%"),
            color_discrete_map={'Germany': '#EF4444', 'France': '#10B981', 'Spain': '#38BDF8'},
            labels={'Rate': 'Tỷ lệ Churn (%)', 'Geography': 'Quốc gia'}
        )
        fig_geo.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0'), showlegend=False)
        st.plotly_chart(fig_geo, use_container_width=True)

# ---------------------------------------------------------
# TAB 2: DIAGNOSTIC ANALYTICS
# ---------------------------------------------------------
with t_diag:
    st.markdown("### 🔍 Phân Tích Chẩn Đoán & Biểu Đồ 4 Động Cơ Gây Churn")
    
    d1, d2 = st.columns(2)
    
    with d1:
        st.subheader("📦 1. Tỷ Lệ Churn Theo Số Lượng Sản Phẩm (Cross-Selling Trap)")
        prod_churn = df_bank.groupby('NumOfProducts').agg(
            Total=('Exited', 'count'),
            Rate=('Exited', lambda x: x.mean() * 100)
        ).reset_index()
        
        fig_prod = px.bar(
            prod_churn,
            x='NumOfProducts',
            y='Rate',
            text=prod_churn['Rate'].apply(lambda x: f"{x:.1f}%"),
            color='Rate',
            color_continuous_scale='Reds',
            labels={'NumOfProducts': 'Số lượng Sản phẩm Sử dụng', 'Rate': 'Tỷ lệ Churn (%)'}
        )
        fig_prod.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0'))
        st.plotly_chart(fig_prod, use_container_width=True)

    with d2:
        st.subheader("👵 2. Tỷ Lệ Churn Theo Nhóm Độ Tuổi (Life-cycle Shift)")
        age_churn = df_bank.groupby('AgeGroup').agg(
            Rate=('Exited', lambda x: x.mean() * 100)
        ).reindex(["18-29 (Trẻ)", "30-39 (Trưởng thành)", "40-49 (Trung niên)", "50-59 (Cận hưu trí)", "60+ (Hưu trí)"]).reset_index()
        
        fig_age = px.line(
            age_churn,
            x='AgeGroup',
            y='Rate',
            markers=True,
            text=age_churn['Rate'].apply(lambda x: f"{x:.1f}%"),
            line_shape='linear',
            color_discrete_sequence=['#F59E0B']
        )
        fig_age.update_traces(textposition="top center", line=dict(width=3), marker=dict(size=10))
        fig_age.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0'))
        st.plotly_chart(fig_age, use_container_width=True)

    st.markdown("---")
    
    d3, d4 = st.columns(2)
    
    with d3:
        st.subheader("💤 3. Tỷ Lệ Churn Theo Trạng Thái Hoạt Động (Active vs Inactive)")
        act_churn = df_bank.groupby('ActiveStatus').agg(
            Rate=('Exited', lambda x: x.mean() * 100)
        ).reset_index()
        
        fig_act = px.pie(
            act_churn,
            names='ActiveStatus',
            values='Rate',
            hole=0.4,
            color='ActiveStatus',
            color_discrete_map={'Inactive': '#EF4444', 'Active': '#10B981'}
        )
        fig_act.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0'))
        st.plotly_chart(fig_act, use_container_width=True)

    with d4:
        st.subheader("💰 4. Tỷ Lệ Churn Theo Trạng Thái Số Dư Tài Khoản")
        df_bank['BalanceSegment'] = df_bank['Balance'].apply(lambda b: "Số dư = 0€" if b == 0 else ("Số dư > 100k€" if b > 100000 else "Số dư 1-100k€"))
        bal_seg = df_bank.groupby('BalanceSegment').agg(
            Rate=('Exited', lambda x: x.mean() * 100)
        ).reset_index()
        
        fig_bal = px.bar(
            bal_seg,
            x='BalanceSegment',
            y='Rate',
            text=bal_seg['Rate'].apply(lambda x: f"{x:.1f}%"),
            color_discrete_sequence=['#38BDF8']
        )
        fig_bal.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#E2E8F0'))
        st.plotly_chart(fig_bal, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: CUSTOMER RISK SCORING
# ---------------------------------------------------------
with t_risk:
    st.markdown("### 🚨 Mô Hình Phân Tầng Rủi Ro & Danh Sách Cần Can Thiệp Kịp Thời")
    st.caption("Gán nhãn điểm rủi ro (Risk Score 0 - 100) để đội ngũ chi nhánh và telesales chủ động liên hệ trước khi khách hàng đóng tài khoản.")
    
    r_col1, r_col2, r_col3 = st.columns([2, 2, 3])
    with r_col1:
        sel_risk = st.selectbox("Lọc Mức Độ Rủi Ro", ["Tất cả mức rủi ro", "Rất Cao (Critical)", "Cao (High)", "Trung Bình (Medium)", "Thấp (Low)"])
    with r_col2:
        sel_country = st.selectbox("Lọc Theo Quốc Gia", ["Tất cả quốc gia", "Germany", "France", "Spain"])
    with r_col3:
        search_cust = st.text_input("🔍 Tìm CustomerID hoặc Họ tên", value="")

    df_risk = df_bank.copy()
    if sel_risk != "Tất cả mức rủi ro":
        df_risk = df_risk[df_risk['RiskLevel'] == sel_risk]
    if sel_country != "Tất cả quốc gia":
        df_risk = df_risk[df_risk['Geography'] == sel_country]
    if search_cust.strip():
        q = search_cust.strip().lower()
        df_risk = df_risk[
            df_risk['CustomerId'].astype(str).str.contains(q) |
            df_risk['Surname'].astype(str).str.lower().str.contains(q)
        ]

    st.markdown(f"**Hiển thị {len(df_risk):,} / {len(df_bank):,} khách hàng**")
    
    st.dataframe(
        df_risk[['CustomerId', 'Surname', 'Geography', 'Gender', 'Age', 'Balance', 'NumOfProducts', 'IsActiveMember', 'RiskScore', 'RiskLevel', 'ChurnStatus']],
        column_config={
            "CustomerId": st.column_config.TextColumn("ID Khách Hàng"),
            "Surname": st.column_config.TextColumn("Họ"),
            "Geography": st.column_config.TextColumn("Quốc Gia"),
            "Age": st.column_config.NumberColumn("Tuổi", format="%d"),
            "Balance": st.column_config.NumberColumn("Số Dư (€)", format="€%.2f"),
            "NumOfProducts": st.column_config.NumberColumn("Số SP", format="%d"),
            "RiskScore": st.column_config.ProgressColumn("Risk Score", min_value=0, max_value=100, format="%d điểm"),
            "RiskLevel": st.column_config.TextColumn("Cấp Rủi Ro"),
            "ChurnStatus": st.column_config.TextColumn("Trạng Thái")
        },
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------------
# TAB 4: SOLUTIONS & EXECUTIVE DECISIONS
# ---------------------------------------------------------
with t_sol:
    st.markdown("### 💡 Bảng Giải Pháp & Quyết Định Chiến Lược Trình Ban Giám Đốc")
    st.caption("Các quyết định quản trị cốt lõi được xây dựng trên kết quả phân tích 5 Whys & Fishbone Diagram")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("🎯 4 QUYẾT ĐỊNH CHIẾN LƯỢC CẦN BAN GIÁM ĐỐC PHÊ DUYỆT")
    
    dec1, dec2 = st.columns(2)
    
    with dec1:
        st.markdown("""
        <div class="decision-card" style="border-left-color: #EF4444;">
            <div class="decision-title">1. Tái Cấu Trúc Gói Bán Chép & Loại Bỏ "Bẫy Sản Phẩm"</div>
            <div class="decision-desc">
                • <strong>Quyết định:</strong> Dừng ngay việc giao KPI bán chéo gói 3–4 sản phẩm rác cho nhân viên sales. Tập trung chuẩn hóa <strong>Gói Chuẩn 2 Sản Phẩm</strong> (có tỷ lệ Churn thấp kỷ lục 7.58%).<br>
                • <strong>Hành động:</strong> Xóa bỏ phí quản lý duy trì tài khoản ở sản phẩm thứ 3 và 4. Rà soát chất lượng sản phẩm bổ sung.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="decision-card" style="border-left-color: #F59E0B;">
            <div class="decision-title">2. Bản Địa Hóa Chính Sách Cho Thị Trường Đức (Germany Taskforce)</div>
            <div class="decision-desc">
                • <strong>Quyết định:</strong> Thành lập ban dự án đặc nhiệm bản địa hóa chính sách cạnh tranh riêng cho chi nhánh Đức (nơi Churn 32.44%).<br>
                • <strong>Hành động:</strong> Miễn phí quản lý tài khoản, nâng lãi suất tiền gửi ngắn hạn để cạnh tranh trực tiếp với Fintech đối thủ (N26, Revolut) tại Đức.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with dec2:
        st.markdown("""
        <div class="decision-card" style="border-left-color: #38BDF8;">
            <div class="decision-title">3. Ra Mắt Gói "Tài Chính Hưu Trí" Cho Nhóm 50–59 Tuổi</div>
            <div class="decision-desc">
                • <strong>Quyết định:</strong> Xây dựng danh mục sản phẩm tư vấn quản lý tài sản hưu trí (Wealth & Retirement Advisory) dành riêng cho độ tuổi 50–59 (Churn 56.04%).<br>
                • <strong>Hành động:</strong> Bố trí Chuyên viên chăm sóc riêng (Personal Relationship Manager) và tối giản giao diện Mobile Banking cho người lớn tuổi.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="decision-card" style="border-left-color: #10B981;">
            <div class="decision-title">4. Điều Chỉnh Cơ Chế Thưởng KPI & Tích Hợp Risk Score</div>
            <div class="decision-desc">
                • <strong>Quyết định:</strong> Gắn KPI thưởng của nhân viên bán hàng với <strong>Tỷ lệ giữ chân khách hàng (Retention Rate)</strong>Thay vì chỉ thưởng theo số lượng hợp đồng mở mới.<br>
                • <strong>Hành động:</strong> Tích hợp tự động chỉ số Risk Score vào phần mềm giao dịch viên để cảnh báo sớm khách hàng rủi ro.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    st.subheader("🧮 MÔ PHỎNG HIỆU QUẢ TÀI CHÍNH (ROI SIMULATOR)")
    
    sim_col1, sim_col2 = st.columns([2, 3])
    
    with sim_col1:
        st.markdown("#### ⚙️ Cấu Hình Giữ Chân")
        retention_rate = st.slider("Tỷ lệ giữ chân thành công nhóm rủi ro (%)", min_value=10, max_value=80, value=40, step=5)
        avg_cost_per_cust = st.number_input("Chi phí giữ chân trung bình (€ / khách)", value=50, step=10)
        
    with sim_col2:
        saved_customers = int(churned_cust * (retention_rate / 100))
        saved_balance = total_lost_balance * (retention_rate / 100)
        total_campaign_cost = saved_customers * avg_cost_per_cust
        net_roi = saved_balance - total_campaign_cost
        
        st.markdown(f"""
        <div style="background: #1E293B; border-radius: 12px; padding: 20px; border: 1px solid #10B981;">
            <h4 style="color: #10B981; margin-top:0;">💰 Kết Quả Dự Báo Tài Chính (Financial ROI):</h4>
            <p>• Số khách hàng giữ chân thành công: <strong>{saved_customers:,} người</strong></p>
            <p>• Số dư tiền gửi giữ lại được: <strong>€{saved_balance:,.2f} (~€{saved_balance/1e6:.1f}M)</strong></p>
            <p>• Tổng chi phí chiến dịch giữ chân: <strong>€{total_campaign_cost:,.2f}</strong></p>
            <h3 style="color: #10B981; margin-bottom:0;">👉 Lợi Nhuận Ròng Thu Về (Net Value Saved): €{net_roi/1e6:.2f}M</h3>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 5: EXPORT REPORT
# ---------------------------------------------------------
with t_exp:
    st.markdown("### 📥 Xuất Báo Cáo Dữ Liệu Bàn Giao Ban Giám Đốc")
    st.caption("Xuất file Excel đầy đủ dữ liệu sạch, điểm rủi ro Risk Score và tóm tắt chiến lược.")
    
    def generate_bank_excel(df_exp):
        wb = openpyxl.Workbook()
        ws1 = wb.active
        ws1.title = "Cleaned_Master_Data"
        
        ws1.views.sheetView[0].showGridLines = True
        
        headers = list(df_exp.columns)
        ws1.append(headers)
        
        header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
        header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        thin_border = Border(
            left=Side(style='thin', color='D9D9D9'),
            right=Side(style='thin', color='D9D9D9'),
            top=Side(style='thin', color='D9D9D9'),
            bottom=Side(style='thin', color='D9D9D9')
        )
        
        for col_num in range(1, len(headers) + 1):
            cell = ws1.cell(row=1, column=col_num)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border
            
        for r_idx, row in df_exp.iterrows():
            ws1.append(list(row.values))
            
        # Summary Sheet
        ws2 = wb.create_sheet(title="Executive_Summary")
        ws2.views.sheetView[0].showGridLines = True
        ws2.append(["Chỉ Số Trọng Yếu", "Giá Trị"])
        ws2.append(["Tổng số khách hàng", len(df_exp)])
        ws2.append(["Số khách hàng Churned", len(df_exp[df_exp['Exited']==1])])
        ws2.append(["Tỷ lệ Churn tổng thể", f"{(len(df_exp[df_exp['Exited']==1])/len(df_exp)*100):.2f}%"])
        ws2.append(["Tổng số dư thất thoát", f"€{df_exp[df_exp['Exited']==1]['Balance'].sum():,.2f}"])
        
        out = io.BytesIO()
        wb.save(out)
        return out.getvalue()

    excel_data = generate_bank_excel(df_bank)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        label="📥 Tải File Báo Cáo Excel Executive (.xlsx)",
        data=excel_data,
        file_name="Bao_Cao_Executive_Bank_Churn_Solutions.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

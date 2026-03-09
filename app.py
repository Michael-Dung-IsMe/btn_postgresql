import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from streamlit_option_menu import option_menu

# Import hàm kéo dữ liệu từ file database_queries.py vừa tạo
from database_queries import fetch_all_gis_data

# ===============================
# 1. CẤU HÌNH TRANG
# ===============================
st.set_page_config(page_title="Hệ thống Quản lý Rác thải GIS", layout="wide")

# ===============================
# 2. ĐỊNH DẠNG GIAO DIỆN (DARK MODE)
# ===============================
st.markdown("""
<style>
.stApp {background-color:#0e1117;}
.metric-card {
    background:#161b22;
    padding:15px;
    border-radius:10px;
    border-left:4px solid #00d1b2;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 3. TẢI DỮ LIỆU TỪ DATABASE (Đã được chuẩn hóa)
# ===============================
@st.cache_data
def load_data():
    """
    Sử dụng cơ chế cache của Streamlit để lưu tạm dữ liệu. 
    Chỉ vào database lấy đúng 1 lần khi người dùng mới mở web.
    """
    bounds, road, garbage, building_res, building_ind = fetch_all_gis_data()
    
    if bounds is None:
        st.error("❌ Không thể lấy dữ liệu từ cơ sở dữ liệu. Vui lòng kiểm tra lại file .env")
        
    return bounds, road, garbage, building_res, building_ind

bounds, road, garbage, building_res, building_ind = load_data()

if bounds is None:
    st.stop() # Dừng chạy web nếu không có dữ liệu

# ===============================
# 4. MENU CHÍNH (PHÍA TRÊN)
# ===============================
selected = option_menu(
    menu_title=None,
    options=["📍 Bản đồ & Điều khiển", "📊 Báo cáo Phân tích"],
    icons=["map", "graph-up-arrow"],
    orientation="horizontal",
    styles={
        "container": {"background-color": "#161b22"},
        "nav-link-selected": {"background-color": "#00d1b2", "color": "#0e1117"},
    },
)

# ===============================
# TRANG 1: BẢN ĐỒ
# ===============================
if selected == "📍 Bản đồ & Điều khiển":

    col_ctrl, col_map = st.columns([1, 3])

    with col_ctrl:
        st.subheader("⚙️ Bảng Điều Khiển")

        mode = st.radio(
            "Chế độ hiển thị",
            [
                "Tất cả dữ liệu",
                "Nhấn mạnh Khu dân cư",
                "Nhấn mạnh Khu công nghiệp",
                "Chỉ hiển thị Điểm rác"
            ]
        )

        buffer_size = st.slider(
            "Vùng đệm rác (mét)",
            0, 500, 0
        )

        st.info("💡 Mẹo: Kéo thanh trượt để xem phạm vi phục vụ của các điểm thu gom rác.")

    with col_map:
        fig, ax = plt.subplots(figsize=(10, 7))
        fig.patch.set_facecolor("#161b22")
        ax.set_facecolor("#161b22")

        # Màu sắc quy chuẩn
        c_res = "#00d1b2"    # Xanh ngọc - Cư dân
        c_ind = "#ffdd57"    # Vàng - Công nghiệp
        c_gar = "#ff3860"    # Đỏ - Điểm rác
        c_road = "#484f58"   # Xám - Đường xá

        # Vẽ lớp nền (Ranh giới & Đường)
        bounds.plot(ax=ax, color="#0d1117", edgecolor="#30363d")
        road.plot(ax=ax, color=c_road, linewidth=0.6, alpha=0.5)

        # Logic hiển thị theo chế độ
        if mode == "Tất cả dữ liệu":
            building_res.plot(ax=ax, color=c_res, alpha=0.5, label="Cư dân")
            building_ind.plot(ax=ax, color=c_ind, alpha=0.5, label="Công nghiệp")
            garbage.plot(ax=ax, color=c_gar, markersize=70, marker="*")

        elif mode == "Nhấn mạnh Khu dân cư":
            building_res.plot(ax=ax, color=c_res, alpha=0.8)
            garbage.plot(ax=ax, color=c_gar, markersize=50)

        elif mode == "Nhấn mạnh Khu công nghiệp":
            building_ind.plot(ax=ax, color=c_ind, alpha=0.8)
            garbage.plot(ax=ax, color=c_gar, markersize=50)

        elif mode == "Chỉ hiển thị Điểm rác":
            garbage.plot(ax=ax, color=c_gar, markersize=120, marker="P")

        # Hiển thị Buffer (Vùng phục vụ)
        if buffer_size > 0:
            garbage.buffer(buffer_size).plot(
                ax=ax,
                color=c_gar,
                alpha=0.2
            )

        ax.set_axis_off()
        st.pyplot(fig, use_container_width=True)

# ===============================
# TRANG 2: THỐNG KÊ & PHÂN TÍCH
# ===============================
else:
    st.header("📊 Báo cáo Tổng hợp & Phân tích Hệ thống")
    
    # --- TÍNH TOÁN DỮ LIỆU ---
    # Tính khoảng cách từ mỗi nhà dân đến điểm rác gần nhất
    dist_series = building_res.geometry.apply(lambda x: garbage.distance(x).min())
    avg_dist = dist_series.mean()
    max_dist = dist_series.max()
    
    # --- HIỂN THỊ 4 CHỈ SỐ VÀNG ---
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric("Tổng điểm rác", f"{len(garbage)} điểm", help="Tổng số điểm thu gom rác thực tế")
    with c2:
        st.metric("Tổng số nhà dân", f"{len(building_res)} căn", help="Tổng số tòa nhà thuộc loại cư dân")
    with c3:
        st.metric("Tổng khu công nghiệp", f"{len(building_ind)} khu", help="Tổng số nhà máy, xí nghiệp")
    with c4:
        st.metric(
            "Khoảng cách trung bình", 
            f"{avg_dist:.2f} m", 
            delta=f"Xa nhất: {max_dist:.1f}m", 
            delta_color="inverse",
            help="Khoảng cách trung bình người dân phải đi bộ đến điểm rác"
        )

    st.markdown("---")
    
    # --- CHI TIẾT PHÂN TÍCH ---
    col_analysis, col_chart = st.columns([1, 1])
    
    with col_analysis:
        st.subheader("📏 Đánh giá khả năng tiếp cận")
        
        # Nhận xét tự động
        if avg_dist < 100:
            st.success("✅ **Hệ thống phân bổ tốt:** Hầu hết cư dân đều ở rất gần các điểm thu gom rác.")
        elif avg_dist < 200:
            st.warning("⚠️ **Mức độ trung bình:** Một số khu vực có thể cần bổ sung thêm thùng rác.")
        else:
            st.error("🚨 **Cần cải thiện:** Khoảng cách tiếp cận quá xa, người dân gặp khó khăn khi đổ rác.")
            
        st.write(f"""
        **Chi tiết kỹ thuật:**
        - Mỗi điểm rác phục vụ trung bình cho **{len(building_res)/len(garbage):.1f}** hộ dân.
        - Tòa nhà nằm ở vị trí bất lợi nhất cần đi bộ **{max_dist:.1f} mét**.
        """)
        
        show_detail = st.checkbox("Hiển thị biểu đồ biến thiên chi tiết")
            
    with col_chart:
        st.subheader("📈 Cơ cấu Hạ tầng")
        df_counts = pd.DataFrame({
            "Loại công trình": ["Cư dân", "Công nghiệp"],
            "Số lượng": [len(building_res), len(building_ind)]
        }).set_index("Loại công trình")
        st.bar_chart(df_counts)

    if show_detail:
        st.divider()
        st.subheader("📉 Biểu đồ khoảng cách tiếp cận của từng khu vực")
        st.area_chart(dist_series)
        st.info("Biểu đồ thể hiện mức độ chênh lệch khoảng cách. Các đỉnh cao đại diện cho các ngôi nhà nằm xa điểm tập kết rác nhất.")

    # DANH SÁCH DỮ LIỆU GỐC
    st.divider()
    with st.expander("📋 Xem danh sách dữ liệu gốc (Điểm rác)"):
        # Loại bỏ cột hình học 'geom' để bảng hiển thị sạch sẽ
        df_display = garbage.drop(columns='geom') if 'geom' in garbage.columns else garbage
        st.dataframe(df_display, use_container_width=True)
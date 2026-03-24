import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches
from streamlit_option_menu import option_menu

from database_queries import fetch_all_gis_data

# ===============================
# 1. CẤU HÌNH TRANG
# ===============================
st.set_page_config(page_title="Hệ thống Quản lý Rác thải GIS", layout="wide")

st.markdown("""
<style>
.stApp {background-color:#0e1117;}
.metric-card {
    background:#161b22;
    padding:15px;
    border-radius:10px;
    border-left:4px solid #00ea75;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 2. TẢI VÀ XỬ LÝ DỮ LIỆU
# ===============================
@st.cache_data
def load_data():
    bounds, road, garbage, building_res, building_ind = fetch_all_gis_data()
    return bounds, road, garbage, building_res, building_ind


@st.cache_data
def calculate_distances(_building_res, _garbage):
    # Tính khoảng cách
    distances = _building_res.geometry.apply(lambda x: _garbage.distance(x).min())
    _building_res['min_dist'] = distances
    
    # Hàm gán màu theo khoảng cách
    def assign_color(dist):
        if dist <= 50: return '#00ea75'    # Xanh lá (Rất gần)
        elif dist <= 150: return '#ffc107' # Vàng (Trung bình)
        else: return '#ff3860'             # Đỏ (Xa)
        
    _building_res['dist_color'] = _building_res['min_dist'].apply(assign_color)
    return _building_res

bounds, road, garbage, building_res_raw, building_ind = load_data()

if bounds is None:
    st.error("❌ Không thể kết nối cơ sở dữ liệu.")
    st.stop()

building_res = calculate_distances(building_res_raw, garbage)

# ===============================
# 3. MENU CHÍNH
# ===============================
selected = option_menu(
    menu_title=None,
    options=["📍 Bản đồ & Điều khiển", "📊 Báo cáo Phân tích"],
    icons=["map", "graph-up-arrow"],
    orientation="horizontal",
    styles={
        "container": {"background-color": "#161b22"},
        "nav-link-selected": {"background-color": "#00ea75", "color": "#0e1117"},
    },
)

# ===============================
# TRANG 1: BẢN ĐỒ LAYER CONTROL
# ===============================
if selected == "📍 Bản đồ & Điều khiển":

    col_ctrl, col_map = st.columns([1, 3])

    with col_ctrl:
        st.subheader("⚙️ Bảng Điều Khiển")

        danh_sach_lop = ["Khu dân cư (Theo khoảng cách)", "Khu công nghiệp", "Điểm thu gom rác", "Hệ thống đường xá"]
        
        lop_hien_thi = st.multiselect(
            "Chọn các lớp dữ liệu muốn hiển thị:",
            options=danh_sach_lop,
            default=["Khu dân cư (Theo khoảng cách)", "Điểm thu gom rác", "Hệ thống đường xá"]
        )

        buffer_size = st.slider("Vùng đệm rác (mét)", 0, 500, 0)
        
        # Chú giải bản đồ
        st.markdown("---")
        st.write("📌 **Chú giải Khu dân cư:**")
        st.markdown("🟢 < 50m (Rất gần)<br>🟡 50m - 150m (Trung bình)<br>🔴 > 150m (Quá xa)", unsafe_allow_html=True)

    with col_map:
        fig, ax = plt.subplots(figsize=(10, 7))
        fig.patch.set_facecolor("#0e1117")
        ax.set_facecolor("#0e1117")

        # 1. Lớp nền ranh giới
        bounds.plot(ax=ax, color="#161b22", edgecolor="#30363d")

        # 2. Xếp chồng các lớp
        if "Hệ thống đường xá" in lop_hien_thi:
            road.plot(ax=ax, color="#6e7681", linewidth=0.5, alpha=0.5)

        if "Khu công nghiệp" in lop_hien_thi:
            building_ind.plot(ax=ax, color="#bd93f9", alpha=0.7)

        if "Khu dân cư (Theo khoảng cách)" in lop_hien_thi:
            # Tô màu nhà dân
            building_res.plot(ax=ax, color=building_res['dist_color'], alpha=0.8)

        if "Điểm thu gom rác" in lop_hien_thi:
            garbage.plot(ax=ax, color="#00f2fe", markersize=80, marker="*")
            
            if buffer_size > 0:
                garbage.buffer(buffer_size).plot(ax=ax, color="#00f2fe", alpha=0.15)

        ax.set_axis_off()
        # Loại bỏ lề thừa của biểu đồ
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)

# ===============================
# TRANG 2: THỐNG KÊ & PHÂN TÍCH
# ===============================
else:
    st.header("📊 Báo cáo Tổng hợp & Phân phối")
    
    # Số liệu tổng quan
    avg_dist = building_res['min_dist'].mean()
    max_dist = building_res['min_dist'].max()
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Tổng điểm rác", f"{len(garbage)} điểm")
    with c2: st.metric("Tổng số nhà dân", f"{len(building_res)} căn")
    with c3: st.metric("Tổng khu công nghiệp", f"{len(building_ind)} khu")
    with c4: st.metric("Khoảng cách TB", f"{avg_dist:.1f} m", delta=f"Xa nhất: {max_dist:.1f}m", delta_color="inverse")

    st.markdown("---")
    
    # Phân nhóm dữ liệu khoảng cách
    nhom_1 = len(building_res[building_res['min_dist'] <= 50])
    nhom_2 = len(building_res[(building_res['min_dist'] > 50) & (building_res['min_dist'] <= 150)])
    nhom_3 = len(building_res[building_res['min_dist'] > 150])
    tong = len(building_res)

    col_table, col_chart = st.columns([1.2, 1])
    
    with col_table:
        st.subheader("📋 Bảng phân loại mức độ tiếp cận")
        df_class = pd.DataFrame({
            "Phân loại": ["🟢 Rất gần (< 50m)", "🟡 Trung bình (50-150m)", "🔴 Quá xa (> 150m)"],
            "Số lượng nhà": [nhom_1, nhom_2, nhom_3],
            "Tỷ lệ": [f"{(nhom_1/tong)*100:.1f}%", f"{(nhom_2/tong)*100:.1f}%", f"{(nhom_3/tong)*100:.1f}%"]
        })
        st.dataframe(df_class, hide_index=True, use_container_width=True)
        
        with st.expander("**💡Nhận xét**"):
            st.info("Các khu vực đánh dấu màu đỏ (>150m) là những điểm mù (blind-spots) trong hệ thống thu gom, cần ưu tiên khảo sát lắp đặt thêm thùng rác trong giai đoạn quy hoạch tiếp theo.")

    with col_chart:
        st.subheader("📉 Biểu đồ Phân phối")
        
        # Vẽ biểu đồ Bar Chart
        fig_bar, ax_bar = plt.subplots(figsize=(6, 4))
        fig_bar.patch.set_facecolor('#0e1117')
        ax_bar.set_facecolor('#0e1117')
        
        categories = ['< 50m', '50-150m', '> 150m']
        values = [nhom_1, nhom_2, nhom_3]
        colors = ['#00ea75', '#ffc107', '#ff3860']
        
        bars = ax_bar.bar(categories, values, color=colors, alpha=0.8)
        
        # Thêm số liệu trên đầu cột
        for bar in bars:
            yval = bar.get_height()
            ax_bar.text(bar.get_x() + bar.get_width()/2, yval + (max(values)*0.02), int(yval), 
                        ha='center', va='bottom', color='white', fontweight='bold')
            
        ax_bar.tick_params(colors='white')
        ax_bar.spines['top'].set_visible(False)
        ax_bar.spines['right'].set_visible(False)
        ax_bar.spines['left'].set_color('#30363d')
        ax_bar.spines['bottom'].set_color('#30363d')
        
        st.pyplot(fig_bar)

    # Danh sách dữ liệu rác
    # st.divider()
    # with st.expander("📋 Xem danh sách tọa độ Điểm rác (Database)"):
    #     df_display = garbage.drop(columns='geom') if 'geom' in garbage.columns else garbage
    #     st.dataframe(df_display, use_container_width=True)
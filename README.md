# 🌍 Bài tập nhóm DBMS - Hệ thống Quản lý Rác thải GIS (Web GIS Application) sử dụng PostgreSQL

## 🧑‍💻 Thành viên

- Phạm Mạnh Dũng - B23DCCE024
- Hoàng Tiến Đạt - B23DCCE015
- Nguyễn Thành Tâm - B23DCCE084

## 🔰 Tổng quan

Đây là ứng dụng Web GIS được xây dựng để trực quan hóa và phân tích dữ liệu không gian về hệ thống thu gom rác thải, ranh giới khu vực, đường giao thông và các công trình (khu dân cư, khu công nghiệp).

Dự án sử dụng **Streamlit** làm giao diện (Frontend + Backend), **PostgreSQL / PostGIS** để lưu trữ và truy vấn dữ liệu không gian, và **Matplotlib / GeoPandas** để render bản đồ.

---

Dưới đây là mẫu file README.md được thiết kế chuẩn mực và chuyên nghiệp, bám sát đúng workflow của nhóm và sử dụng matplotlib để vẽ bản đồ như bạn yêu cầu.

Bạn chỉ cần tạo một file tên là README.md trong thư mục gốc của dự án và copy toàn bộ nội dung dưới đây vào:

Markdown

# 🌍 Hệ thống Quản lý Rác thải GIS (Web GIS)

Đây là ứng dụng Web GIS được xây dựng bằng **Streamlit**, **GeoPandas** và **Matplotlib**, kết hợp với cơ sở dữ liệu không gian **PostgreSQL / PostGIS**. Ứng dụng cho phép trực quan hóa bản đồ, đánh giá phạm vi phục vụ của các điểm thu gom rác và phân tích khoảng cách tiếp cận của khu dân cư/khu công nghiệp.

---

## 📂 Cấu trúc thư mục

```text
my-webgis-project/
│
├── data/                       # Thư mục chứa dữ liệu
|   ├── garbage.zio             # Chứa các file .shp, .dbf gốc
│   └── database_dump.sql       # File backup dữ liệu PostGIS (dùng để restore)
│
├── app.py                      # Giao diện chính và logic xử lý (Streamlit + Matplotlib)
├── database_queries.py         # File chứa các hàm kết nối và truy vấn PostgreSQL
│
├── .env.example                # File mẫu cấu hình biến môi trường
├── requirements.txt            # Danh sách các thư viện Python cần thiết
└── README.md                   # Hướng dẫn cài đặt và khởi chạy
```

---

## ✨ Tính năng chính

- 🗺️ **Hiển thị bản đồ tĩnh:** Sử dụng Matplotlib để vẽ và hiển thị các lớp dữ liệu không gian (Polygon, LineString, Point).
- 🎛️ **Bảng điều khiển tương tác:** Cho phép lọc hiển thị theo khu dân cư, khu công nghiệp và thay đổi bán kính vùng đệm (buffer) của các điểm thu gom rác.
- 📊 **Phân tích không gian:** Tự động tính toán khoảng cách từ các hộ dân đến điểm rác gần nhất và đánh giá mức độ tiếp cận hạ tầng.
- 📈 **Báo cáo thống kê:** Hiển thị biểu đồ và các chỉ số tổng hợp về cơ cấu hạ tầng.

---

## 🛠️ Yêu cầu hệ thống

Để chạy được dự án này trên local, bạn cần cài đặt sẵn:

1. **Python** (phiên bản 3.9 trở lên).
2. **PostgreSQL** và extension **PostGIS** (dùng để xử lý dữ liệu hệ tọa độ).

---

## 🚀 Hướng dẫn Cài đặt & Khởi chạy

### Bước 1: Clone mã nguồn từ GitHub

Mở Terminal / Command Prompt và chạy lệnh sau:

```bash
git clone https://github.com/Michael-Dung-IsMe/btn_postgresql.git
cd btn_postgresql
pip install -r requirements.txt
```

### Bước 2: Khởi tạo Cơ sở dữ liệu (Database)

Mở pgAdmin (hoặc công cụ quản lý DB tương đương).

Tạo một cơ sở dữ liệu mới (ví dụ: exercise_dbms).

Mở Query Tool trên database vừa tạo và chạy lệnh sau để kích hoạt PostGIS:

```sql
CREATE EXTENSION postgis;
```

Restore dữ liệu: Sử dụng công cụ Restore của pgAdmin để nạp file data/database_dump.sql vào cơ sở dữ liệu vừa tạo.

### Bước 3: Cấu hình biến môi trường

Trong thư mục gốc của dự án, nhân bản (copy) file .env.example và đổi tên thành .env.

Mở file .env và điền thông tin đăng nhập PostgreSQL của máy bạn:

```snippet
DB_USER=your_username
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
```

### Bước 4: Khởi chạy Web App

Sau khi cài đặt xong thư viện, khởi động server Streamlit bằng lệnh:

```bash
streamlit run app.py
```

Trình duyệt sẽ tự động mở trang web tại địa chỉ http://localhost:8501.

Dự án được xây dựng nhằm hoàn thành bài tập Hệ quản trị Cơ sở dữ liệu.

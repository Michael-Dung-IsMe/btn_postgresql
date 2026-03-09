# 🌍 Bài tập nhóm DBMS - Hệ thống Quản lý Rác thải GIS (Web GIS Application) sử dụng PostgreSQL

## 🧑‍💻 Thành viên

- Phạm Mạnh Dũng - B23DCCE024
- Hoàng Tiến Đạt - B23DCCE015
- Nguyễn Thành Tâm - B23DCCE084

## 🔰 Tổng quan

Đây là ứng dụng Web GIS được xây dựng để trực quan hóa và phân tích dữ liệu không gian về hệ thống thu gom rác thải, ranh giới khu vực, đường giao thông và các công trình (khu dân cư, khu công nghiệp).

Dự án sử dụng **Streamlit** làm giao diện (Frontend + Backend), **PostgreSQL / PostGIS** để lưu trữ và truy vấn dữ liệu không gian, và **Matplotlib / GeoPandas** để render bản đồ.

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
git clone
cd
```

import os
import geopandas as gpd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Tải các biến môi trường từ file .env
load_dotenv()

def get_db_connection():
    """Tạo chuỗi kết nối an toàn đến PostgreSQL bằng SQLAlchemy"""
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")
    
    # Chuẩn URL kết nối của SQLAlchemy
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
    return engine

def fetch_all_gis_data():
    """Hàm gọi SQL để kéo toàn bộ 5 bảng dữ liệu không gian lên Web"""
    engine = get_db_connection()
    
    try:
        # Dùng geopandas.read_postgis để lấy dữ liệu qua SQL
        bounds = gpd.read_postgis("SELECT * FROM bounds", engine, geom_col="geom")
        road = gpd.read_postgis("SELECT * FROM road", engine, geom_col="geom")
        garbage = gpd.read_postgis("SELECT * FROM garbadge", engine, geom_col="geom")
        
        building_res = gpd.read_postgis(
            "SELECT * FROM building WHERE nature LIKE '%%Residential%%'", 
            engine, geom_col="geom"
        )
        
        building_ind = gpd.read_postgis(
            "SELECT * FROM building WHERE nature LIKE '%%Industrial%%'", 
            engine, geom_col="geom"
        )
        
        return bounds, road, garbage, building_res, building_ind
        
    except Exception as e:
        print(f"❌ Lỗi truy xuất dữ liệu từ PostGIS: {e}")
        return None, None, None, None, None
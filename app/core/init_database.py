from app.core.database import engine, Base
from app.models.models import Client, Device, SensorData, Alert

def init_database():
    print("Đang kết nối tới cơ sở dữ liệu và khởi tạo các bảng...")
    # Lệnh này sẽ tự động quét qua các class Model và tạo bảng trong PostgreSQL nếu chưa tồn tại
    Base.metadata.create_all(bind=engine)
    print("Khởi tạo và tạo thành công toàn bộ 4 bảng: clients, devices, sensor_data, alerts!")

if __name__ == "__main__":
    init_database()
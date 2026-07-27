from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Boolean, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key= True, index = True, autoincrement=True)
    client_id = Column(String, unique=True, index=True, nullable=False)
    company_name = Column(String, unique=True, nullable=False)
    contact_email = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    devices = relationship("Device", back_populates="client")

class Device(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_serial = Column(String, unique=True, index=True, nullable=False)
    hardware_model = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    client = relationship("Client", back_populates="devices")
    sensor_data = relationship("SensorData", back_populates="device")
    alerts = relationship("Alert", back_populates = "device")

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("device.id"), nullable=False)

    power_kw = Column(Float, nullable=False)
    temperature_c = Column(Float, nullable=False)
    voltage = Column(Float, nullable=True)

    optimal_baseline = Column(Float, nullable=True)
    is_anomaly = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    device = relationship("Device", back_populates="sensor_data")

    __table_args__ = (Index('idx_device_created_at', 'device_id', 'created_at'),)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index= True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("device.id"), nullable=False)
    deviation_value = Column(Float, nullable=False)
    created_at = Column(DateTime, default = lambda: datetime.now(timezone.utc))

    device = relationship("Device", back_populates = "alerts")
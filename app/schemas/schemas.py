from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List


# --- CLIENT SCHEMAS ---
class ClientBase(BaseModel):
    company_name: str
    contact_email: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int


# --- DEVICE SCHEMAS ---
class DeviceBase(BaseModel):
    device_serial: str
    hardware_model: str
    client_id: int

class DeviceCreate(DeviceBase):
    pass

class DeviceResponse(DeviceBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int


# --- SENSOR DATA SCHEMAS ---
class SensorDataCreate(BaseModel):
    device_id: int
    power_kw: float
    temperature_c: float
    voltage: Optional[float] = None
    optimal_baseline: Optional[float] = None
    is_anomaly: bool = False

class SensorDataBatchCreate(BaseModel):
    readings: List[SensorDataCreate]

class SensorDataResponse(SensorDataCreate):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime


# --- ALERT SCHEMAS ---
class AlertCreate(BaseModel):
    device_id: int
    deviation_value: float

class AlertResponse(AlertCreate):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime


# --- PASSWORD CHANGE SCHEMA ---
class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
from datetime import datetime, timedelta, timezone
from app.models.models import Alert, Client, Device, SensorData
from app.schemas.schemas import AlertCreate, ClientCreate, DeviceCreate, SensorDataCreate, ChangePasswordRequest
from app.security.hashing import Hash

import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


# ---- CLIENT'S CRUD ----
async def get_client(db: AsyncSession, client_id: int):
    """Retrieve a single active client by ID."""
    result = await db.execute(
        select(Client).filter(
            Client.id == client_id, Client.is_active == True
        )
    )
    return result.scalars().first()


async def get_clients(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Retrieve a paginated list of active clients."""
    result = await db.execute(
        select(Client).filter(Client.is_active == True).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_client(db: AsyncSession, client: ClientCreate):
    """Create a new client record in the database."""
    # Tự động sinh client_id và băm mật khẩu mặc định nếu schema không bắt buộc hoặc chưa cung cấp
    generated_client_id = getattr(client, "client_id", None) or f"client_{uuid.uuid4().hex[:8]}"
    hashed_pwd = getattr(client, "password", None) and Hash.bcrypt(client.password) or Hash.bcrypt("DefaultPassword123")

    db_client = Client(
        client_id=generated_client_id,
        company_name=client.company_name,
        contact_email=client.contact_email,
        hashed_password=hashed_pwd,
        is_active=True
    )
    db.add(db_client)
    await db.commit()
    await db.refresh(db_client)
    return db_client


async def soft_delete_client(db: AsyncSession, client_id: int):
    """Soft delete a client by marking them as inactive and setting the deletion timestamp."""
    result = await db.execute(
        select(Client).filter(
            Client.id == client_id, Client.is_active == True
        )
    )
    db_client = result.scalars().first()
    if db_client:
        db_client.is_active = False
        db_client.deleted_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(db_client)
    return db_client


async def restore_client(db: AsyncSession, client_id: int):
    """Restore a soft-deleted client back to active status."""
    result = await db.execute(
        select(Client).filter(
            Client.id == client_id, Client.is_active == False
        )
    )
    db_client = result.scalars().first()
    if db_client:
        db_client.is_active = True
        db_client.deleted_at = None
        await db.commit()
        await db.refresh(db_client)
    return db_client


async def purge_old_deleted_clients(db: AsyncSession, days_old: int = 30):
    """Permanently delete clients that have been soft-deleted for longer than the specified days."""
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)
    result = await db.execute(
        select(Client).filter(
            Client.is_active == False, Client.deleted_at < cutoff_date
        )
    )
    clients_to_purge = result.scalars().all()
    deleted_rows = len(clients_to_purge)
    for client in clients_to_purge:
        await db.delete(client)
    await db.commit()
    return deleted_rows

async def update_client_password(db: AsyncSession, client_id: int, passwords: ChangePasswordRequest):
    """Verify old password and update with a new hashed password for the client."""
    # 1. Query to find the active client by ID in the database
    result = await db.execute(select(Client).filter(Client.id == client_id, Client.is_active == True))
    db_client = result.scalars().first()

    # Return None if the client does not exit
    if not db_client:
        return None

    # 2. Verify if the provided old password matches the hashed password stored in DB
    if not Hash.verify(passwords.old_password, db_client.hashed_password):
        return False

    # 3. Hash the new password and update the client record
    db_client.hashed_password = Hash.bcrypt(passwords.new_password)

    # Commit changes the database and refresh the client instance
    await db.commit()
    await db.refresh(db_client)

    return True



# ---- DEVICE'S CRUD ----
async def get_device(db: AsyncSession, device_id: int):
    """Retrieve a single active device by ID."""
    result = await db.execute(
        select(Device).filter(
            Device.id == device_id, Device.is_active == True
        )
    )
    return result.scalars().first()


async def get_devices(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Retrieve a paginated list of active devices."""
    result = await db.execute(
        select(Device).filter(Device.is_active == True).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_device(db: AsyncSession, device: DeviceCreate):
    """Create a new hardware device linked to a client."""
    db_device = Device(
        device_serial=device.device_serial,
        hardware_model=device.hardware_model,
        client_id=device.client_id,
    )
    db.add(db_device)
    await db.commit()
    await db.refresh(db_device)
    return db_device


async def soft_delete_device(db: AsyncSession, device_id: int):
    """Soft delete a device by marking it inactive and recording the deletion time."""
    result = await db.execute(
        select(Device).filter(
            Device.id == device_id, Device.is_active == True
        )
    )
    db_device = result.scalars().first()
    if db_device:
        db_device.is_active = False
        db_device.deleted_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(db_device)
    return db_device


async def restore_device(db: AsyncSession, device_id: int):
    """Restore a soft-deleted device to active status."""
    result = await db.execute(
        select(Device).filter(
            Device.id == device_id, Device.is_active == False
        )
    )
    db_device = result.scalars().first()
    if db_device:
        db_device.is_active = True
        db_device.deleted_at = None
        await db.commit()
        await db.refresh(db_device)
    return db_device


async def purge_old_deleted_devices(db: AsyncSession, days_old: int = 30):
    """Permanently remove devices soft-deleted beyond the retention period."""
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)
    result = await db.execute(
        select(Device).filter(
            Device.is_active == False, Device.deleted_at < cutoff_date
        )
    )
    devices_to_purge = result.scalars().all()
    deleted_rows = len(devices_to_purge)
    for device in devices_to_purge:
        await db.delete(device)
    await db.commit()
    return deleted_rows


# ---- SENSOR DATA'S CRUD ----
async def create_sensor_data(db: AsyncSession, data: SensorDataCreate):
    """Save a single telemetry sensor reading record."""
    db_sensor = SensorData(
        device_id=data.device_id,
        power_kw=data.power_kw,
        temperature_c=data.temperature_c,
        voltage=data.voltage,
        optimal_baseline=data.optimal_baseline,
        is_anomaly=data.is_anomaly
    )
    db.add(db_sensor)
    await db.commit()
    await db.refresh(db_sensor)
    return db_sensor


async def create_sensor_data_batch(db: AsyncSession, batch_data):
    """Save a batch of telemetry sensor reading records to optimize database overhead."""
    db_records = []
    for reading in batch_data.readings:
        db_sensor = SensorData(
            device_id=reading.device_id,
            power_kw=reading.power_kw,
            temperature_c=reading.temperature_c,
            voltage=reading.voltage,
            optimal_baseline=reading.optimal_baseline,
            is_anomaly=reading.is_anomaly
        )
        db.add(db_sensor)
        db_records.append(db_sensor)
    
    await db.commit()
    for record in db_records:
        await db.refresh(record)
    return db_records


async def get_sensor_data_by_device(
    db: AsyncSession, device_id: int, skip: int = 0, limit: int = 100
):
    """Retrieve telemetry history for a specific device with pagination."""
    result = await db.execute(
        select(SensorData)
        .filter(SensorData.device_id == device_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def delete_old_sensor_data(db: AsyncSession, days_old: int = 90):
    """Delete historical sensor readings older than the retention threshold to save storage."""
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)
    result = await db.execute(
        select(SensorData).filter(SensorData.created_at < cutoff_date)
    )
    sensors_to_purge = result.scalars().all()
    deleted_rows = len(sensors_to_purge)
    for sensor in sensors_to_purge:
        await db.delete(sensor)
    await db.commit()
    return deleted_rows


# ---- ALERT'S CRUD ----
async def create_alert(db: AsyncSession, alert: AlertCreate):
    """Create a new system anomaly or alert record."""
    db_alert = Alert(
        device_id=alert.device_id, deviation_value=alert.deviation_value
    )
    db.add(db_alert)
    await db.commit()
    await db.refresh(db_alert)
    return db_alert


async def get_alerts(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Retrieve a paginated list of system alerts."""
    result = await db.execute(select(Alert).offset(skip).limit(limit))
    return result.scalars().all()


async def delete_old_alerts(db: AsyncSession, days_old: int = 90):
    """Delete historical alerts older than the specified retention days."""
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)
    result = await db.execute(
        select(Alert).filter(Alert.created_at < cutoff_date)
    )
    alerts_to_purge = result.scalars().all()
    deleted_rows = len(alerts_to_purge)
    for alert in alerts_to_purge:
        await db.delete(alert)
    await db.commit()
    return deleted_rows
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.crud import crud

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])


@router.delete("/purge-old-data/")
async def purge_old_data(db: AsyncSession = Depends(get_db)):
  deleted_clients = await crud.purge_old_deleted_clients(db=db, days_old=30)
  deleted_devices = await crud.purge_old_deleted_devices(db=db, days_old=30)
  deleted_sensors = await crud.delete_old_sensor_data(db=db, days_old=90)
  deleted_alerts = await crud.delete_old_alerts(db=db, days_old=90)
  return {
      "message": "Cleanup executed successfully.",
      "purged_clients": deleted_clients,
      "purged_devices": deleted_devices,
      "purged_sensor_data_rows": deleted_sensors,
      "purged_alert_rows": deleted_alerts,
  }
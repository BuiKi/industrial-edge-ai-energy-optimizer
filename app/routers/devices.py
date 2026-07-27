from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.post("/", response_model=schemas.DeviceResponse)
async def create_device(
    device: schemas.DeviceCreate, db: AsyncSession = Depends(get_db)
):
  return await crud.create_device(db=db, device=device)


@router.get("/", response_model=list[schemas.DeviceResponse])
async def read_devices(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
  return await crud.get_devices(db, skip=skip, limit=limit)


@router.delete("/{device_id}/")
async def soft_delete_device(device_id: int, db: AsyncSession = Depends(get_db)):
  db_device = await crud.soft_delete_device(db=db, device_id=device_id)
  if not db_device:
    raise HTTPException(
        status_code=404, detail="Device not found or already inactive"
    )
  return {
      "message": f"Device with id {device_id} has been soft deleted successfully."
  }


@router.put("/{device_id}/restore/", response_model=schemas.DeviceResponse)
async def restore_device(device_id: int, db: AsyncSession = Depends(get_db)):
  db_device = await crud.restore_device(db=db, device_id=device_id)
  if not db_device:
    raise HTTPException(
        status_code=404, detail="Device not found or not in deleted state"
    )
  return db_device
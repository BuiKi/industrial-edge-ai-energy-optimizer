from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.post("/", response_model=schemas.AlertResponse)
async def create_alert(
    alert: schemas.AlertCreate, db: AsyncSession = Depends(get_db)
):
  return await crud.create_alert(db=db, alert=alert)


@router.get("/", response_model=list[schemas.AlertResponse])
async def read_alerts(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
  return await crud.get_alerts(db, skip=skip, limit=limit)
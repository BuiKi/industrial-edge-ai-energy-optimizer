from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas import schemas
from app.crud import crud

router = APIRouter(prefix="/sensor-data", tags=["Sensor Telemetry"])


class ConnectionManager:
    """Manager to handle active WebSocket connections for real-time telemetry broadcasting."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept incoming WebSocket connection and register it."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Unregister and remove disconnected WebSocket client."""
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Broadcast telemetry payloads to all active WebSocket clients."""
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@router.post("/", response_model=schemas.SensorDataResponse, status_code=status.HTTP_201_CREATED)
async def create_sensor_data(
    data: schemas.SensorDataCreate, db: AsyncSession = Depends(get_db)
):
    """Ingest a single high-frequency sensor telemetry record and broadcast it in real-time."""
    new_record = await crud.create_sensor_data(db=db, data=data)
    
    # Broadcast live telemetry event to dashboard clients (e.g., Streamlit)
    await manager.broadcast({
        "event": "NEW_SENSOR_DATA",
        "device_id": new_record.device_id,
        "power_kw": new_record.power_kw,
        "temperature_c": new_record.temperature_c,
        "is_anomaly": new_record.is_anomaly
    })
    
    return new_record


@router.post("/batch", response_model=list[schemas.SensorDataResponse], status_code=status.HTTP_201_CREATED)
async def create_sensor_data_batch(
    batch_data: schemas.SensorDataBatchCreate, db: AsyncSession = Depends(get_db)
):
    """Ingest a batch of telemetry records to optimize hardware bandwidth and reduce request overhead."""
    created_records = await crud.create_sensor_data_batch(db=db, batch_data=batch_data)
    
    # Broadcast batch ingestion notification
    await manager.broadcast({
        "event": "NEW_BATCH_DATA",
        "count": len(created_records)
    })
    
    return created_records


@router.get("/", response_model=list[schemas.SensorDataResponse])
async def read_sensor_data(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """Retrieve paginated global sensor telemetry records."""
    return await crud.get_sensor_data(db=db, skip=skip, limit=limit)


@router.get(
    "/devices/{device_id}/sensor-data/",
    response_model=list[schemas.SensorDataResponse],
)
async def read_sensor_data_by_device(
    device_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve filtered telemetry records specific to a target industrial device ID."""
    return await crud.get_sensor_data_by_device(
        db=db, device_id=device_id, skip=skip, limit=limit
    )


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint to establish persistent bi-directional streaming for live dashboard updates."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and listen for incoming client frames if necessary
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
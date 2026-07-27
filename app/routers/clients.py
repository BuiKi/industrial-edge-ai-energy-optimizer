from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.schemas import ClientCreate, ClientResponse, ChangePasswordRequest
from app.crud.crud import create_client, get_clients, soft_delete_client, restore_client, update_client_password
from app.models.models import Client
from app.security.hashing import Hash
from app.security.permissions import get_current_client, verify_infrastructure_admin

router = APIRouter(prefix="/clients", tags=["Clients Management"])


# --- INFRASTRUCTURE ADMIN ENDPOINTS (Restricted) ---

@router.post("/", response_model=ClientResponse, dependencies=[Depends(verify_infrastructure_admin)])
async def api_create_client(
    client: ClientCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new client (Restricted to Infrastructure Admins only)."""
    return await create_client(db=db, client=client)


@router.get("/", response_model=list[ClientResponse], dependencies=[Depends(verify_infrastructure_admin)])
async def api_read_clients(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """Retrieve all clients (Restricted to Infrastructure Admins only)."""
    return await get_clients(db, skip=skip, limit=limit)


@router.delete("/{client_id}/", dependencies=[Depends(verify_infrastructure_admin)])
async def api_soft_delete_client(client_id: int, db: AsyncSession = Depends(get_db)):
    """Soft delete a client by ID (Restricted to Infrastructure Admins only)."""
    db_client = await soft_delete_client(db=db, client_id=client_id)
    if not db_client:
        raise HTTPException(
            status_code=404, detail="Client not found or already inactive"
        )
    return {
        "message": f"Client with id {client_id} has been soft deleted successfully."
    }


@router.put("/{client_id}/restore/", response_model=ClientResponse, dependencies=[Depends(verify_infrastructure_admin)])
async def api_restore_client(client_id: int, db: AsyncSession = Depends(get_db)):
    """Restore a soft-deleted client (Restricted to Infrastructure Admins only)."""
    db_client = await restore_client(db=db, client_id=client_id)
    if not db_client:
        raise HTTPException(
            status_code=404, detail="Client not found or not in deleted state"
        )
    return db_client


# --- CLIENT SELF-SERVICE ENDPOINTS ---

@router.put("/change-password")
async def change_password(
    body: ChangePasswordRequest,
    current_client: Client = Depends(get_current_client),
    db: AsyncSession = Depends(get_db),
):
    """Allows the authenticated client to securely change their own password."""
    
    result = await update_client_password(db=db, client_id=current_client.id, passwords=body)
    
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect old password"
        )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Client not found"
        )

    return {"message": "Password changed successfully."}
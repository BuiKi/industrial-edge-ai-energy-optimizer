from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.models import Client
from app.security.jwt import verify_access_token

# Initialize OAuth2 scheme pointing to login route
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Credentials exception template
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

async def get_current_client(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
) -> Client:
    """Verify incoming token and retrieve the authenticated client instance."""
    client_id = verify_access_token(token, credentials_exception)

    result = await db.execute(select(Client).where(Client.client_id== client_id))
    client = result.scalars().first()
    if client is None:
        raise credentials_exception
    return client

async def verify_infrastructure_admin(token: str = Depends(oauth2_scheme)):
    """Verify if the requester has infrastructure admin privileges.
    Infrastructure admins can manage clients/maintenance but cannot inspect client sensor data.
    """
    payload = verify_access_token(token, credentials_exception)
    
    # Trích xuất role từ payload của token
    role = payload.get("role")

    # Enforce role-based restriction for infrastructure management only
    if role != "infrastructure_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Infrastructure admin privileges required."
        )
    return payload

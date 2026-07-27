from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.models import Client
from app.security.hashing import Hash
from app.security.jwt import create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm= Depends(),
    db: AsyncSession = Depends(get_db)):
    """Authenticate client credentials and return a JWT access token."""

  # 1. Find the client in the database by username (client_id)
    result = await db.execute(select(Client).where(Client.client_id == form_data.username))
    client= result.scalars().first()

    # 2. Validate client existence and password hash using Hash.verify()
    if not client or not Hash.verify(form_data.password, client.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Incorrect client ID or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 3. Create JWT access token containing client identifier in 'sub' payload
    access_token = create_access_token(data={"sub": str(client.client_id)})

    # 4. Return the token back to the client/device
    return {"access_token": access_token, "token_type": "bearer"}





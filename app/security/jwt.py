from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.core.config import settings

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Generate a new JWT access token containing client payload and expiration time."""
    to_encode = data.copy()

    # Set token expiration time
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Encode the token using the secret key and designated algorithm
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode_jwt

def verify_access_token(token: str, credentials_exception):
    """Verify incoming JWT token and extract payload safely."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        client_id: str = payload.get("sub")
        if client_id is None:
            raise credentials_exception
        return payload  # Trả về toàn bộ payload dictionary thay vì chỉ mỗi client_id
    except JWTError:
        raise credentials_exception
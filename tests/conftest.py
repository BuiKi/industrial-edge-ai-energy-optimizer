import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from main import app
from app.core.database import get_db, Base
from app.models.models import Client
from app.security.hashing import Hash

# Sử dụng SQLite in-memory (:memory:) để test chạy nhanh và độc lập
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def override_get_db():
    """Ghi đè hàm kết nối DB chính bằng DB test in-memory."""
    async with TestingSessionLocal() as session:
        yield session

# Ép FastAPI dùng DB test tạm thời khi chạy pytest
app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    """Tự động tạo bảng trước mỗi bài test và xóa sạch sau khi test xong."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def async_client():
    """Cung cấp client HTTP giả lập để gọi trực tiếp các API trong ứng dụng."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture
async def authenticated_client(async_client):
    """Fixture tạo client chuẩn trong DB test và gắn JWT token có quyền admin vào header."""
    from app.security.jwt import create_access_token
    from app.security.hashing import Hash

    # 1. Tạo client trong DB
    async with TestingSessionLocal() as session:
        new_client = Client(
            client_id="test_client_01",
            company_name="Industrial Corp Test",
            contact_email="contact@industrial.com",
            hashed_password=Hash.bcrypt("StrongPassword123"),
            is_active=True
        )
        session.add(new_client)
        await session.commit()

    # 2. Tạo token mang sub và thêm "role": "infrastructure_admin" để vượt qua 403 Forbidden
    token = create_access_token(data={
        "sub": "test_client_01",
        "role": "infrastructure_admin"
    })
    
    # 3. Gắn vào header
    async_client.headers = {"Authorization": f"Bearer {token}"}
    
    yield async_client
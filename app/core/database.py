from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Tạo async engine sử dụng DATABASE_URL đã được cấu hình trong file .env (có dạng postgresql+asyncpg://...)
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Tạo session maker cho async
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


# Dependency để lấy database session bất đồng bộ cho các API endpoint
async def get_db():
  async with SessionLocal() as session:
    try:
      yield session
      await session.commit()
    except Exception:
      await session.rollback()
      raise
    finally:
      await session.close()
      
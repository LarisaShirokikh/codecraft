# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Создаем асинхронный движок для PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Создаем фабрику асинхронных сессий
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Добавляем алиас SessionLocal для обратной совместимости
SessionLocal = AsyncSessionLocal

print(f"Using DATABASE_URL: {settings.DATABASE_URL}")  # DEBUG

# Функция-зависимость для FastAPI, возвращающая сессию БД
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
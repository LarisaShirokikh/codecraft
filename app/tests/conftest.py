import asyncio
import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
import pytest_asyncio

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.base import Base
from app.db.session import engine, AsyncSessionLocal
from app.main import app
from app.api.deps import get_db
from app.models.users import User

# Создаем тестовую схему в существующей PostgreSQL БД
TEST_SCHEMA = "test_schema"

# Переопределяем event loop для асинхронных тестов
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Создаем и удаляем тестовую схему
@pytest.fixture(scope="session")
async def setup_database():
    # Создаем схему и все таблицы
    async with engine.begin() as conn:
        # Создаем тестовую схему если ее еще нет
        await conn.execute(f"CREATE SCHEMA IF NOT EXISTS {TEST_SCHEMA}")
        # Устанавливаем схему по умолчанию для текущего соединения
        await conn.execute(f"SET search_path TO {TEST_SCHEMA}")
        # Создаем все таблицы в тестовой схеме
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Удаляем тестовую схему после всех тестов
    async with engine.begin() as conn:
        await conn.execute(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA} CASCADE")

# Получаем тестовую сессию БД с установленной схемой
@pytest.fixture
async def db_session(setup_database) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        # Устанавливаем схему для сессии
        await session.execute(f"SET search_path TO {TEST_SCHEMA}")
        
        # Очищаем таблицы перед каждым тестом
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(f"TRUNCATE TABLE {TEST_SCHEMA}.{table.name} RESTART IDENTITY CASCADE")
        
        await session.commit()
        
        yield session
        
        # Откат изменений после теста
        await session.rollback()

# Переопределяем зависимость БД для FastAPI
@pytest.fixture
async def override_get_db(db_session: AsyncSession):
    async def _override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = _override_get_db
    yield
    # Восстанавливаем оригинальную зависимость
    del app.dependency_overrides[get_db]

# Фикстура для HTTP клиента
@pytest.fixture
async def client(override_get_db) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# Фикстура для создания обычного пользователя
@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    # Создаем нового пользователя для теста
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("password123"),
        is_active=True,
        is_superuser=False
    )
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    return user

# Фикстура для создания администратора
@pytest.fixture
async def admin_user(db_session: AsyncSession) -> User:
    # Создаем нового администратора для теста
    admin = User(
        email="admin@example.com",
        username="admin",
        hashed_password=get_password_hash("password123"),
        is_active=True,
        is_superuser=True
    )
    
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    
    return admin
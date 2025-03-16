import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.users import User

BASE_URL = "/api/v1/users"

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, db_session: AsyncSession):
    """
    Тест регистрации нового пользователя
    """
    response = await client.post(f"{BASE_URL}/", json={
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "password123"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data

    # Проверяем, что пользователь появился в БД
    result = await db_session.execute(
        select(User).where(User.email == "newuser@example.com")
    )
    user = result.scalars().first()
    assert user is not None

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, test_user: User):
    """
    Тест логина зарегистрированного пользователя
    """
    response = await client.post("/api/v1/login/access-token", data={
        "username": test_user.email,
        "password": "password123"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    return data["access_token"]

@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, test_user: User):
    """
    Тест получения данных текущего пользователя (GET /me)
    """
    # Логинимся и получаем токен
    login_response = await client.post("/api/v1/login/access-token", data={
        "username": test_user.email,
        "password": "password123"
    })
    access_token = login_response.json()["access_token"]

    # Запрашиваем данные пользователя
    response = await client.get(f"{BASE_URL}/me", headers={"Authorization": f"Bearer {access_token}"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["username"] == test_user.username

@pytest.mark.asyncio
async def test_update_user_me(client: AsyncClient, test_user: User, db_session: AsyncSession):
    """
    Тест обновления данных текущего пользователя
    """
    # Логинимся и получаем токен
    login_response = await client.post("/api/v1/login/access-token", data={
        "username": test_user.email,
        "password": "password123"
    })
    access_token = login_response.json()["access_token"]

    # Обновляем данные пользователя
    response = await client.put(
        f"{BASE_URL}/me", 
        json={
            "username": "updated_username",
            "email": "updated@example.com"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated@example.com"
    assert data["username"] == "updated_username"

    # Проверяем, что данные обновились в БД
    result = await db_session.execute(select(User).where(User.id == test_user.id))
    updated_user = result.scalars().first()
    assert updated_user.email == "updated@example.com"
    assert updated_user.username == "updated_username"

@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient, test_user: User, admin_user: User):
    """
    Тест получения данных пользователя по ID
    """
    # Логинимся как админ и получаем токен
    login_response = await client.post("/api/v1/login/access-token", data={
        "username": admin_user.email,
        "password": "password123"
    })
    access_token = login_response.json()["access_token"]

    # Запрашиваем данные другого пользователя
    response = await client.get(
        f"{BASE_URL}/{test_user.id}", 
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["username"] == test_user.username

@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient, test_user: User):
    """
    Тест на запрет доступа без авторизации
    """
    response = await client.get(f"{BASE_URL}/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, test_user: User, admin_user: User, db_session: AsyncSession):
    """
    Тест удаления пользователя (требуется права админа)
    """
    # Логинимся как админ
    login_response = await client.post("/api/v1/login/access-token", data={
        "username": admin_user.email,
        "password": "password123"
    })
    admin_token = login_response.json()["access_token"]

    # Отправляем запрос на удаление пользователя
    response = await client.delete(
        f"{BASE_URL}/{test_user.id}", 
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 204  # No Content (успешное удаление)

    # Проверяем, что пользователя больше нет в БД
    result = await db_session.execute(select(User).where(User.id == test_user.id))
    user = result.scalars().first()
    assert user is None

@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, test_user: User, admin_user: User, db_session: AsyncSession):
    """
    Тест обновления пользователя админом
    """
    # Логинимся как админ
    login_response = await client.post("/api/v1/login/access-token", data={
        "username": admin_user.email,
        "password": "password123"
    })
    admin_token = login_response.json()["access_token"]

    # Обновляем данные другого пользователя
    response = await client.put(
        f"{BASE_URL}/{test_user.id}", 
        json={
            "username": "admin_updated",
            "email": "admin_updated@example.com"
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin_updated@example.com"
    assert data["username"] == "admin_updated"

    # Проверяем, что данные обновились в БД
    result = await db_session.execute(select(User).where(User.id == test_user.id))
    updated_user = result.scalars().first()
    assert updated_user.email == "admin_updated@example.com"
    assert updated_user.username == "admin_updated"
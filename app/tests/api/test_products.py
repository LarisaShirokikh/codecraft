# test_products.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Фикстура для создания тестовой категории
@pytest.fixture(scope="module")
def test_category():
    # Создаем тестовую категорию через соответствующий эндпоинт.
    # Убедитесь, что эндпоинт для создания категории существует и работает.
    payload = {
        "name": "Test Category"
    }
    response = client.post("/api/v1/categories/", json=payload)
    assert response.status_code == 201, f"Ошибка создания категории: {response.text}"
    return response.json()

def test_create_product(test_category):
    # Тестируем создание продукта
    payload = {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 100,
        "stock": 10,
        "category_id": test_category["id"],
        "is_active": True
    }
    response = client.post("/api/v1/products/", json=payload)
    assert response.status_code == 201, f"Ошибка создания продукта: {response.text}"
    data = response.json()
    assert "id" in data
    assert data["name"] == payload["name"]

def test_get_product(test_category):
    # Создаем продукт, а затем получаем его по ID
    payload = {
        "name": "Another Test Product",
        "description": "This is another test product",
        "price": 150,
        "stock": 5,
        "category_id": test_category["id"],
        "is_active": True
    }
    response_create = client.post("/api/v1/products/", json=payload)
    assert response_create.status_code == 201, f"Ошибка создания продукта: {response_create.text}"
    created_product = response_create.json()
    product_id = created_product["id"]

    response_get = client.get(f"/api/v1/products/{product_id}")
    assert response_get.status_code == 200, f"Ошибка получения продукта: {response_get.text}"
    data = response_get.json()
    assert data["id"] == product_id
    assert data["name"] == payload["name"]

def test_update_product(test_category):
    # Создаем продукт, затем обновляем его
    payload = {
        "name": "Update Test Product",
        "description": "Product before update",
        "price": 200,
        "stock": 15,
        "category_id": test_category["id"],
        "is_active": True
    }
    response_create = client.post("/api/v1/products/", json=payload)
    assert response_create.status_code == 201, f"Ошибка создания продукта: {response_create.text}"
    created_product = response_create.json()
    product_id = created_product["id"]

    update_payload = {
        "name": "Updated Test Product",
        "description": "Product after update",
        "price": 250,
        "stock": 20,
        "is_active": False
    }
    response_update = client.put(f"/api/v1/products/{product_id}", json=update_payload)
    assert response_update.status_code == 200, f"Ошибка обновления продукта: {response_update.text}"
    updated_product = response_update.json()
    assert updated_product["name"] == update_payload["name"]
    assert updated_product["description"] == update_payload["description"]
    assert updated_product["price"] == update_payload["price"]
    assert updated_product["stock"] == update_payload["stock"]
    assert updated_product["is_active"] == update_payload["is_active"]

def test_delete_product(test_category):
    # Создаем продукт, затем удаляем его и проверяем, что он больше не доступен
    payload = {
        "name": "Delete Test Product",
        "description": "Product to be deleted",
        "price": 300,
        "stock": 5,
        "category_id": test_category["id"],
        "is_active": True
    }
    response_create = client.post("/api/v1/products/", json=payload)
    assert response_create.status_code == 201, f"Ошибка создания продукта: {response_create.text}"
    created_product = response_create.json()
    product_id = created_product["id"]

    response_delete = client.delete(f"/api/v1/products/{product_id}")
    assert response_delete.status_code == 200, f"Ошибка удаления продукта: {response_delete.text}"
    delete_response = response_delete.json()
    assert "message" in delete_response

    # Проверяем, что продукт действительно удален
    response_get = client.get(f"/api/v1/products/{product_id}")
    assert response_get.status_code == 404, "Продукт не удален"
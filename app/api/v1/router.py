# router.py           # Основной роутер API v1
# app/api/v1/router.py
from fastapi import APIRouter

from app.api.v1.endpoints import login, products, categories, catalogs, users

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(catalogs.router, prefix="/catalogs", tags=["catalogs"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(login.router, tags=["login"])
# api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
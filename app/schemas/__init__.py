# File: app/schemas/__init__.py
# Make sure this file exists and imports/re-exports all your schemas

from app.schemas.product_schema import ProductBase, ProductCreate, ProductUpdate, ProductResponse
from app.schemas.catalog_schema import CatalogBase, CatalogCreate, CatalogUpdate, CatalogResponse
from app.schemas.category_schema import CategoryBase, CategoryCreate, CategoryUpdate, CategoryResponse
from app.schemas.feature_schema import ProductFeatureCreate, ProductFeatureResponse
from app.schemas.photo_schema import ProductPhotoCreate, ProductPhotoResponse
from app.schemas.video_schema import ProductVideoCreate, ProductVideoResponse
from app.schemas.user_schema import UserCreate, UserResponse
# from app.schemas.order_schema import OrderCreate, OrderResponse

# If you need to re-export for type hints
from typing import List, Optional

# File: app/api/v1/endpoints/products.py (the beginning part with imports)
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app import schemas  # This should now have ProductResponse
# from app.crud import product_crud
# ... rest of your imports
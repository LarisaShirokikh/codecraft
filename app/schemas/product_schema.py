# Product schemas
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.schemas.catalog_schema import CatalogResponse
from app.schemas.category_schema import CategoryResponse
from app.schemas.feature_schema import ProductFeatureCreate, ProductFeatureResponse
from app.schemas.photo_schema import ProductPhotoResponse
from app.schemas.video_schema import ProductVideoResponse

class ProductBase(BaseModel):
    name: str
    new_price: int
    old_price: Optional[int] = None
    in_stock: bool = True
    description: Optional[str] = None

class ProductCreate(ProductBase):
    catalog_id: int
    category_ids: List[int] = []
    features: List[ProductFeatureCreate] = []
    
class ProductUpdate(ProductBase):
    catalog_id: Optional[int] = None
    category_ids: Optional[List[int]] = None

class ProductResponse(ProductBase):
    id: int
    catalog_id: int
    catalog: Optional[CatalogResponse] = None
    categories: List[CategoryResponse] = []
    features: List[ProductFeatureResponse] = []
    photos: List[ProductPhotoResponse] = []
    videos: List[ProductVideoResponse] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
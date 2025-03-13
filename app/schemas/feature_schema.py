# Feature schema
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class ProductFeatureBase(BaseModel):
    name: str
    value: str

class ProductFeatureCreate(ProductFeatureBase):
    pass

class ProductFeatureResponse(ProductFeatureBase):
    id: int
    product_id: int
    
    class Config:
        from_attributes = True
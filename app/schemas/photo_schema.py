from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

# Photo schema
class ProductPhotoBase(BaseModel):
    url: str
    
class ProductPhotoCreate(ProductPhotoBase):
    pass

class ProductPhotoResponse(ProductPhotoBase):
    id: int
    product_id: int
    
    class Config:
        from_attributes = True
# Video schema
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class ProductVideoBase(BaseModel):
    url: str
    
class ProductVideoCreate(ProductVideoBase):
    pass

class ProductVideoResponse(ProductVideoBase):
    id: int
    product_id: int
    
    class Config:
        from_attributes = True
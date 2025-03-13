# Category schema
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    # можно добавить дополнительные поля, если нужно
    pass

class CategoryUpdate(CategoryBase):
    # можно добавить дополнительные поля, если нужно
    pass

class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True
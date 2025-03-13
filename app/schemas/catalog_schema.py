# Catalog schema for response
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class CatalogBase(BaseModel):
    name: str

class CatalogCreate(CatalogBase):
    # можно добавить дополнительные поля, если нужно
    pass

class CatalogUpdate(CatalogBase):
    # можно добавить дополнительные поля, если нужно
    pass

class CatalogResponse(CatalogBase):
    id: int
    
    class Config:
        from_attributes = True
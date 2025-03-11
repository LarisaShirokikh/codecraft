from typing import List, Optional

from pydantic import BaseModel

class ProductFeatureCreate(BaseModel):
    name: str  # Название характеристики
    value: str  # Значение характеристики

class ProductFeatureResponse(BaseModel):
    id: int
    name: str
    value: str

    class Config:
        from_attributes = True  # Ранее называлось `orm_mode = True`

class ProductCreate(BaseModel):
    name: str  # Название продукта
    price: float  # Цена
    in_stock: bool = True  # В наличии (по умолчанию True)
    description: Optional[str] = None  # Описание (опционально)
    category_id: int  # ID категории
    features: List[ProductFeatureCreate]  # Список характеристик

class ProductFeatureResponse(BaseModel):
    id: int
    name: str
    value: str

    class Config:
        from_attributes = True  # Ранее называлось `orm_mode = True`
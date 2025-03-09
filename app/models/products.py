from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from . import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # Название
    price = Column(Float, nullable=False)  # Цена
    in_stock = Column(Boolean, default=True)  # В наличии или нет
    description = Column(Text, nullable=True)  # Описание
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)  # Категория

    category = relationship("Category", back_populates="products")
    features = relationship("ProductFeature", back_populates="product", cascade="all, delete-orphan")
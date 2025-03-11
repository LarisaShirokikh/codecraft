from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from app.models import Base

# Промежуточная таблица для связи "многие ко многим" (продукт - категории)
category_product = Table(
    "category_product",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # Название
    new_price = Column(Integer, nullable=False)
    old_price = Column(Integer, nullable=True)
    in_stock = Column(Boolean, default=True)  # В наличии или нет
    description = Column(Text, nullable=True)  # Описание
    catalog_id = Column(Integer, ForeignKey("catalogs.id"), nullable=False)  # Каталог

    photos = relationship("ProductPhoto", back_populates="product", cascade="all, delete-orphan")
    videos = relationship("ProductVideo", back_populates="product", cascade="all, delete-orphan")
    features = relationship("ProductFeature", back_populates="product", cascade="all, delete-orphan")

    categories = relationship("Category", secondary="category_product", back_populates="products")
    catalog = relationship("Catalog", back_populates="products")
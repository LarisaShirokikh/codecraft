from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models import Base

# Ассоциативная таблица для связи "многие ко многим" (Категории <-> Продукты)
product_category_association = Table(
    "product_category_association",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id", ondelete="CASCADE")),
    # Change this
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE")),  # Not "category.id"
)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Each category belongs to one catalog
    catalog_id = Column(Integer, ForeignKey("catalogs.id", ondelete="CASCADE"), nullable=True)
    catalog = relationship("Catalog", back_populates="categories")  # Note the plural "categories" here
    
    # Many-to-many relationship with products
    products = relationship("Product", secondary="category_product", back_populates="categories")
    
    # Relationship with photos
    photos = relationship("CategoryPhoto", back_populates="category", cascade="all, delete-orphan")
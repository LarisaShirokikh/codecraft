from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.models import Base

# Ассоциативная таблица для связи "многие ко многим" (Категории <-> Продукты)
product_category_association = Table(
    "product_category_association",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id", ondelete="CASCADE")),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE")),
)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # Название категории

    # Связь с каталогом (Используем use_alter=True для разрыва цикла)
    catalog_id = Column(Integer, ForeignKey("catalogs.id", use_alter=True, ondelete="CASCADE"), nullable=True)

    catalog = relationship("Catalog", back_populates="categories", foreign_keys=[catalog_id])
    products = relationship("Product", secondary=product_category_association, back_populates="categories")

    # Добавляем связь с фото
    photos = relationship("CategoryPhoto", back_populates="category", cascade="all, delete-orphan")
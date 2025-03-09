from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from . import Base

class ProductFeature(Base):
    __tablename__ = "product_features"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)  # Название характеристики
    value = Column(Text, nullable=False)  # Значение

    product = relationship("Product", back_populates="features")
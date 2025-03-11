from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class ProductPhoto(Base):
    __tablename__ = "product_photos"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    url = Column(String, nullable=False)  # Ссылка на фото
    alt_text = Column(String, nullable=True)  # Описание фото (например, "вид сзади")

    product = relationship("Product", back_populates="photos")
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)  # Рейтинг от 1 до 5
    user_id = Column(Integer, ForeignKey("users.id"))  # Кто оставил отзыв
    product_id = Column(Integer, ForeignKey("products.id"))  # Для какого продукта

    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")
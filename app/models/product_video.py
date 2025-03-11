from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base


class ProductVideo(Base):
    __tablename__ = "product_videos"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    url = Column(String, nullable=False)  # Ссылка на видео (YouTube/Vimeo или mp4)
    description = Column(String, nullable=True)  # Описание видео

    product = relationship("Product", back_populates="videos")
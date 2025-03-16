from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base


class CategoryPhoto(Base):
    __tablename__ = "category_photos"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    url = Column(String, nullable=False)  # URL изображения

    category = relationship("Category", back_populates="photos")
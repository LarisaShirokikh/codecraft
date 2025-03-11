from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base

class Catalog(Base):
    __tablename__ = "catalogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  
    
    category_id = Column(Integer, ForeignKey("categories.id", use_alter=True, ondelete="CASCADE"), nullable=True)  

    category = relationship("Category", back_populates="catalogs", foreign_keys=[category_id])
    products = relationship("Product", back_populates="catalog")
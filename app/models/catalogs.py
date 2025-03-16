from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base

class Catalog(Base):
    __tablename__ = "catalogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  
    
    
    categories = relationship("Category", back_populates="catalog")
    products = relationship("Product", back_populates="catalog")
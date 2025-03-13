# product.py              # CRUD для Product
# app/crud/product.py
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.products import Product
from app.models.product_features import ProductFeature
from app.models.product_photo import ProductPhoto
from app.models.product_video import ProductVideo
from app.schemas.product import ProductCreate, ProductUpdate, ProductPhotoCreate, ProductVideoCreate, ProductFeatureCreate

class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Product]:
        return db.query(Product).filter(Product.name == name).first()
        
    def get_multi_by_category(
        self, db: Session, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        return (
            db.query(Product)
            .filter(Product.categories.any(id=category_id))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_with_filters(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        catalog_id: Optional[int] = None,
        category_id: Optional[int] = None,
        in_stock: Optional[bool] = None,
        min_price: Optional[int] = None,
        max_price: Optional[int] = None,
        search: Optional[str] = None
    ) -> List[Product]:
        query = db.query(Product)
        
        if catalog_id:
            query = query.filter(Product.catalog_id == catalog_id)
        
        if category_id:
            query = query.filter(Product.categories.any(id=category_id))
        
        if in_stock is not None:
            query = query.filter(Product.in_stock == in_stock)
        
        if min_price is not None:
            query = query.filter(Product.new_price >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.new_price <= max_price)
        
        if search:
            query = query.filter(Product.name.ilike(f"%{search}%"))
        
        return query.offset(skip).limit(limit).all()
        
    # Методы для связанных сущностей
    def add_photo(self, db: Session, *, product_id: int, photo_in: ProductPhotoCreate) -> ProductPhoto:
        db_obj = ProductPhoto(
            product_id=product_id,
            url=photo_in.url,
            alt_text=photo_in.alt_text
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def remove_photo(self, db: Session, *, product_id: int, photo_id: int) -> None:
        db_obj = db.query(ProductPhoto).filter(
            ProductPhoto.id == photo_id,
            ProductPhoto.product_id == product_id
        ).first()
        db.delete(db_obj)
        db.commit()

    # Аналогичные методы для видео и характеристик...


product = CRUDProduct(Product)
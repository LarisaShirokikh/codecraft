# app/crud/product.py (асинхронная версия)
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.products import Product
from app.models.categories import Category
from app.models.product_photo import ProductPhoto
from app.schemas.photo_schema import ProductPhotoCreate
from app.schemas.product_schema import ProductCreate, ProductUpdate

class CRUDProduct:
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Product]:
        result = await db.execute(select(Product).where(Product.name == name))
        return result.scalars().first()
        
    async def get_multi_by_category(
        self, db: AsyncSession, *, category_id: int, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        stmt = (
            select(Product)
            .where(Product.categories.any(id=category_id))
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()
    
    async def get_multi_with_filters(
        self, 
        db: AsyncSession, 
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
        stmt = select(Product)
        
        if catalog_id:
            stmt = stmt.where(Product.catalog_id == catalog_id)
        
        if category_id:
            stmt = stmt.where(Product.categories.any(id=category_id))
        
        if in_stock is not None:
            stmt = stmt.where(Product.in_stock == in_stock)
        
        if min_price is not None:
            stmt = stmt.where(Product.new_price >= min_price)
        
        if max_price is not None:
            stmt = stmt.where(Product.new_price <= max_price)
        
        if search:
            stmt = stmt.where(Product.name.ilike(f"%{search}%"))
        
        stmt = stmt.offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()
        
    # Методы для работы с фотографиями
    async def add_photo(self, db: AsyncSession, *, product_id: int, photo_in: ProductPhotoCreate) -> ProductPhoto:
        db_obj = ProductPhoto(
            product_id=product_id,
            url=photo_in.url,
            alt_text=photo_in.alt_text
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def remove_photo(self, db: AsyncSession, *, product_id: int, photo_id: int) -> None:
        stmt = select(ProductPhoto).where(
            ProductPhoto.id == photo_id,
            ProductPhoto.product_id == product_id
        )
        result = await db.execute(stmt)
        db_obj = result.scalars().first()
        if db_obj:
            await db.delete(db_obj)
            await db.commit()

    async def create(self, db: AsyncSession, *, obj_in: ProductCreate) -> Product:
        from app.models.categories import Category
        
        # Convert Pydantic model to dict
        obj_in_data = obj_in.model_dump(exclude_unset=True)

        # Extract category_ids
        category_ids = obj_in_data.pop("category_ids", [])

        # Create Product object
        db_obj = Product(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        # If categories are provided, add them
        if category_ids:
            # Get Category objects one by one and append them
            for cat_id in category_ids:
                stmt = select(Category).where(Category.id == cat_id)
                result = await db.execute(stmt)
                category = result.scalars().first()
                if category:
                    db_obj.categories = db_obj.categories + [category]
            
            # Save changes
            await db.commit()
            await db.refresh(db_obj)

        return db_obj
# Экземпляр CRUD для удобного импорта
product = CRUDProduct()
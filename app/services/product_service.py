from typing import List, Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.products import Product
from app.models.categories import Category
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.core.exceptions import NotFoundError


class ProductService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
    
    async def create_product(self, product_in: ProductCreate) -> ProductResponse:
        """Создать новый продукт"""
        # Проверка существования категории
        category_stmt = select(Category).where(Category.id == product_in.category_id)
        category = await self.db.scalar(category_stmt)
        if not category:
            raise NotFoundError(f"Категория с ID {product_in.category_id} не найдена")
        
        # Создание продукта
        product = Product(
            name=product_in.name,
            description=product_in.description,
            price=product_in.price,
            stock=product_in.stock,
            category_id=product_in.category_id,
            is_active=product_in.is_active
        )
        
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        
        return ProductResponse.model_validate(product)
    
    async def get_product(self, product_id: int) -> ProductResponse:
        """Получить продукт по ID"""
        stmt = (
            select(Product)
            .options(selectinload(Product.category))
            .where(Product.id == product_id)
        )
        product = await self.db.scalar(stmt)
        if not product:
            raise NotFoundError(f"Продукт с ID {product_id} не найден")
        
        return ProductResponse.model_validate(product)
    
    async def update_product(
        self, product_id: int, product_in: ProductUpdate
    ) -> ProductResponse:
        """Обновить существующий продукт"""
        # Проверка существования продукта
        product = await self.get_product(product_id)
        
        # Проверка существования категории, если она изменяется
        if product_in.category_id is not None:
            category_stmt = select(Category).where(Category.id == product_in.category_id)
            category = await self.db.scalar(category_stmt)
            if not category:
                raise NotFoundError(f"Категория с ID {product_in.category_id} не найдена")
        
        # Обновление продукта
        update_data = product_in.model_dump(exclude_unset=True)
        
        stmt = (
            update(Product)
            .where(Product.id == product_id)
            .values(**update_data)
            .returning(Product)
        )
        
        updated_product = await self.db.scalar(stmt)
        await self.db.commit()
        
        # Получаем обновлённый продукт с категорией
        return await self.get_product(product_id)
    
    async def delete_product(self, product_id: int) -> Dict[str, Any]:
        """Удалить продукт"""
        # Проверка существования продукта
        await self.get_product(product_id)
        
        # Удаление продукта
        stmt = delete(Product).where(Product.id == product_id)
        await self.db.execute(stmt)
        await self.db.commit()
        
        return {"message": f"Продукт с ID {product_id} успешно удален"}
    
    async def list_products(
        self,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> List[ProductResponse]:
        """Получить список продуктов с фильтрацией"""
        stmt = select(Product).options(selectinload(Product.category))
        
        # Применяем фильтры
        if category_id is not None:
            stmt = stmt.where(Product.category_id == category_id)
        
        if is_active is not None:
            stmt = stmt.where(Product.is_active == is_active)
        
        # Пагинация
        stmt = stmt.offset(skip).limit(limit)
        
        result = await self.db.scalars(stmt)
        products = result.all()
        
        return [ProductResponse.model_validate(product) for product in products]
# products.py     # CRUD для продуктов
# app/api/v1/endpoints/products.py
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.ProductResponse])
def read_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    catalog_id: Optional[int] = None,
    category_id: Optional[int] = None,
    in_stock: Optional[bool] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    search: Optional[str] = None,
) -> Any:
    """
    Получить список продуктов с возможностью фильтрации.
    """
    products = crud.product.get_multi_with_filters(
        db, 
        skip=skip, 
        limit=limit, 
        catalog_id=catalog_id,
        category_id=category_id,
        in_stock=in_stock,
        min_price=min_price, 
        max_price=max_price,
        search=search
    )
    return products

@router.post("/", response_model=schemas.ProductFeatureResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: schemas.ProductCreate,
) -> Any:
    """
    Создать новый продукт.
    """
    product = crud.product.get_by_name(db, name=product_in.name)
    if product:
        raise HTTPException(
            status_code=400,
            detail=f"Продукт с названием '{product_in.name}' уже существует."
        )
    return crud.product.create(db=db, obj_in=product_in)

# ... остальные эндпоинты
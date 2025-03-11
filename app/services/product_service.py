from sqlalchemy.orm import Session
from app.models.products import Product
from app.models.users import User, UserRole
from app.schemas.product import ProductCreate


def create_product(db: Session, product: ProductCreate, user_id: int):
    if db.query(User).filter(User.id == user_id, User.role == UserRole.ADMIN).first():
        db_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            added_by_id=user_id
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    raise ValueError("Только админы могут добавлять продукты")
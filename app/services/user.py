import bcrypt
from sqlalchemy.orm import Session
from app.models.products import Product

from app.models.users import User, UserRole
from app.schemas.product_schema import ProductCreate
from app.schemas.user_schema import UserCreate

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=UserRole.USER,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_role(db: Session, user_id: int, new_role: UserRole):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.role = new_role
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def can_change_role(current_user: User, target_user: User, new_role: UserRole) -> bool:
    if new_role == UserRole.SUPER_ADMIN and current_user.role != UserRole.SUPER_ADMIN:
        return False
    if current_user.role == UserRole.ADMIN and target_user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        return False
    return True

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

def assign_user_role(db: Session, current_user_id: int, target_user_id: int, new_role: UserRole):
    current_user = db.query(User).filter(User.id == current_user_id).first()
    target_user = db.query(User).filter(User.id == target_user_id).first()

    if not current_user or not target_user:
        raise ValueError("Пользователь не найден")

    # Только супер-админ может назначать роли
    if current_user.role != UserRole.SUPER_ADMIN:
        raise ValueError("Только супер-админ может назначать роли")

    target_user.role = new_role
    db.commit()
    db.refresh(target_user)
    return target_user

async def get_user_by_email(db: AsyncSession, email: str):
    """Получает пользователя по email."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()
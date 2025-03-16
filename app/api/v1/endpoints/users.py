from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr

from app import schemas, models
from app.api import deps
from app.crud.user import user as user_crud
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdate

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(deps.get_db),
):
    user = await user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким email уже существует.",
        )

    username_exists = await user_crud.get_by_username(db, username=user_in.username)
    if username_exists:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким именем уже существует.",
        )

    new_user = await user_crud.create(db=db, obj_in=user_in)
    return UserResponse.model_validate(new_user)

@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: models.User = Depends(deps.get_current_user),
):
    return UserResponse.model_validate(current_user)

@router.put("/me", response_model=UserResponse)
async def update_user_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    password: str = None,
    email: EmailStr = None,
    username: str = None,
    current_user: models.User = Depends(deps.get_current_user),
):
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)

    if password:
        user_in.password = password
    if email is not None:
        user_in.email = email
    if username is not None:
        user_in.username = username

    user = await user_crud.update(db, db_obj=current_user, obj_in=user_in)
    return UserResponse.model_validate(user)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db),
):
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    if current_user.id != user.id and not user_crud.is_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для выполнения операции",
        )

    return UserResponse.model_validate(user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
):
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден",
        )

    user = await user_crud.update(db, db_obj=user, obj_in=user_in)
    return UserResponse.model_validate(user)
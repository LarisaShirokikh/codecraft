# deps.py                 # Зависимости API (авторизация и т.д.)
# app/api/deps.py
from typing import AsyncGenerator, Generator, Optional

from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.core.exceptions import UnauthorizedError, ForbiddenError
from app.db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)


async def get_db() -> AsyncGenerator:
    """
    Зависимость для получения сессии БД.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        await db.close()


def get_current_user(
    security_scopes: SecurityScopes,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> models.User:
    """
    Получает текущего пользователя по JWT токену.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise UnauthorizedError("Некорректные учетные данные")
    
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise UnauthorizedError("Пользователь не найден")
    
    # Проверка scope (прав доступа)
    if security_scopes.scopes:
        token_scopes = token_data.scopes or []
        for scope in security_scopes.scopes:
            if scope not in token_scopes:
                raise ForbiddenError(
                    "Недостаточно прав для выполнения операции"
                )
    
    return user


def get_current_active_user(
    current_user: models.User = Security(get_current_user, scopes=[]),
) -> models.User:
    """
    Проверяет, что пользователь активен.
    """
    if not current_user.is_active:
        raise ForbiddenError("Неактивный пользователь")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Security(get_current_user, scopes=["admin"]),
) -> models.User:
    """
    Проверяет, что пользователь является суперпользователем.
    """
    if not current_user.is_superuser:
        raise ForbiddenError("Требуются права администратора")
    return current_user
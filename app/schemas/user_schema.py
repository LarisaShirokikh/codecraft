from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Импортируем перечисление ролей из модели
class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"

# Общие свойства
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[UserRole] = UserRole.USER

# Свойства для создания пользователя
class UserCreate(UserBase):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

# Свойства для обновления пользователя
class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8)

# Свойства, хранящиеся в БД
class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime

    class Config:
        orm_mode = True

# Свойства для возврата клиенту
class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Схема для токена аутентификации
class Token(BaseModel):
    access_token: str
    token_type: str

# Схема полезной нагрузки токена
class TokenPayload(BaseModel):
    sub: Optional[int] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
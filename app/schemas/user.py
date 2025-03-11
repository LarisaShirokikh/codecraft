from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.models.users import UserRole

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
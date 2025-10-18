from pydantic import BaseModel, EmailStr
from enum import Enum

"""
Pydantic-схемы для валидации и сериализации данных пользователей.
"""

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True

class ResponseSchema(BaseModel):
    status_code: int
    detail: str
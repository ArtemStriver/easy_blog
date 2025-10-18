from fastapi import Response
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from starlette import status

from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token, create_refresh_token
from app.users.crud import get_user_by_email
from app.users.models import User
from app.users.schemas import UserCreate, ResponseSchema, UserRead

"""
Бизнес-логика взаимодействия с базой данных.
Содержит CRUD-функции для регистрации, логина и создания токенов.
Изолирует работу с БД от маршрутов API.
"""

async def register_user(
        db: AsyncSession,
        user_data: UserCreate
) -> ResponseSchema:
    existing = await get_user_by_email(db, user_data.email)
    if existing:
        raise ValueError("User already exists")

    hashed = hash_password(user_data.password)

    stmt = insert(User).values({
        "email": user_data.email,
        "hashed_password": hashed,
    }).returning(User.id)
    await db.execute(stmt)
    await db.commit()

    return ResponseSchema(
        status_code=status.HTTP_201_CREATED,
        detail="user created",
    )

async def authenticate_user(
        db: AsyncSession,
        email: EmailStr,
        password: str
) -> UserRead | None:
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

async def create_tokens(
        response: Response,
        user: UserRead
) -> dict:
    data = {"sub": user.email, "role": user.role}
    access = await create_access_token(response, data)
    refresh = await create_refresh_token(response, data)
    return {"access_token": access, "refresh_token": refresh,"token_type": "bearer"}

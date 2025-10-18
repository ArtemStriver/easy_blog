from typing import List

from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User, UserRole
from app.users.schemas import UserRead, ResponseSchema

"""
Бизнес-логика взаимодействия с базой данных.
Содержит CRUD-функции для User.
Изолирует работу с БД от маршрутов API.
"""

async def get_user_by_email(
        db: AsyncSession,
        user_email: EmailStr | str,
) -> UserRead | None:
    query = select(User).where(User.email == user_email)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_user_by_id(
        db: AsyncSession,
        user_id: int,
) -> UserRead | None:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_all_users(
        db: AsyncSession,
) -> List[UserRead]:
    result = await db.execute(select(User))
    return result.scalars().all()

async def change_role(
        db: AsyncSession,
        user_id: int,
        new_role: UserRole,
) -> UserRead:
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.role = new_role
    await db.commit()
    await db.refresh(user)
    return user

async def delete_user_by_id(
        db: AsyncSession,
        user_id: int,
) -> ResponseSchema:
    stmt = delete(User).where(User.id == user_id)
    await db.execute(stmt)
    await db.commit()
    return ResponseSchema(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="user deleted",
    )

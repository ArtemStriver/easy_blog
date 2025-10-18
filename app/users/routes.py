from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import get_current_user
from app.core.database import get_async_session
from app.users.crud import get_all_users, change_role, get_user_by_id, delete_user_by_id
from app.users.utils import get_current_admin
from app.users.schemas import UserRead, UserRole, ResponseSchema

"""
REST API маршруты для работы с авторизацией и аутентификацией.
Реализует:
--GET /me — узнать свои данные (публичный)
--GET / — список пользователей
--GET /{user_id} — получить данные пользователя 
--PATCH /{user_id}/change_role — изменить роль пользователя
--DELETE /{user_id}/delete_user — удалить пользователя 
"""

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get(
    "/me",
    response_model=UserRead,
)
async def get_me(
        current_user: Annotated[UserRead, Depends(get_current_user)],
) -> UserRead:
    return current_user

@users_router.get(
    "/",
    response_model=List[UserRead],
)
async def get_list_users(
        _: Annotated[UserRead, Depends(get_current_admin)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
) -> List[UserRead]:
    return await get_all_users(db)

@users_router.get(
    "/{user_id}",
    response_model=UserRead,
)
async def get_user(
        _: Annotated[UserRead, Depends(get_current_admin)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
        user_id: int,
) -> UserRead:
    return await get_user_by_id(db, user_id)

@users_router.patch(
    "/{user_id}/change_role",
    response_model=UserRead,
)
async def change_user_role(
        _: Annotated[UserRead, Depends(get_current_admin)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
        user_id: int,
        new_role: UserRole,
) -> UserRead:
    return await change_role(db, user_id, new_role)

@users_router.delete(
    "/{user_id}/delete_user",
    response_model=ResponseSchema,
)
async def delete_user(
        _: Annotated[UserRead, Depends(get_current_admin)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
        user_id: int,
) -> ResponseSchema:
    return await delete_user_by_id(db, user_id)
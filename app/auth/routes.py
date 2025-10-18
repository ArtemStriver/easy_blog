from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth import schemas, crud, utils
from app.core.database import get_async_session
from app.users.schemas import ResponseSchema, UserCreate, UserRead

"""
REST API маршруты для работы с авторизацией и аутентификацией.
Реализует:
--POST /register — регистрация пользователя
--POST /login — авторизация пользователя
--POST /refresh — аутентификация пользователя 
"""

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post(
    "/register",
    response_model=ResponseSchema
)
async def register(
        user_data: UserCreate,
        db: Annotated[AsyncSession, Depends(get_async_session)],
) -> ResponseSchema:
    try:
        return await crud.register_user(db, user_data)
    except ValueError:
        raise HTTPException(status_code=400, detail="User already exists")

@auth_router.post(
    "/login",
    response_model=schemas.Token
)
async def login(
        response: Response,
        user_data: UserCreate,
        db: Annotated[AsyncSession, Depends(get_async_session)],
) -> dict:
    user = await crud.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return await crud.create_tokens(response, user)

@auth_router.post(
    "/refresh"
)
async def refresh(
        response: Response,
        user: Annotated[UserRead, Depends(utils.check_refresh_token)],
) -> dict:
    return await crud.create_tokens(response, user)

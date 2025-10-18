from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.jwt import decode_token
from app.core.database import get_async_session
from app.users.crud import get_user_by_email
from app.users.schemas import UserRead

"""
Вспомогательные функции и утилиты.
Содержит функции проверки рефреш токена и валидности текущего пользователя.
"""

cookies_access_scheme = APIKeyCookie(name=settings.COOKIE_ACCESS_TOKEN_KEY)
cookies_refresh_scheme = APIKeyCookie(name=settings.COOKIE_REFRESH_TOKEN_KEY)

async def check_refresh_token(
        db: Annotated[AsyncSession, Depends(get_async_session)],
        refresh_token: Annotated[str, Depends(cookies_refresh_scheme)],
) -> UserRead:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(refresh_token)
        if payload is None:
            raise credentials_exception
        email: str = payload.get("sub")
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user(
        db: Annotated[AsyncSession, Depends(get_async_session)],
        token: str = Depends(cookies_access_scheme),
) -> UserRead:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        if payload is None:
            raise credentials_exception
        email: str = payload.get("sub")
    except JWTError:
        raise credentials_exception
    user = await get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

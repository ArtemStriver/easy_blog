from fastapi import Response
from datetime import datetime, timedelta
from jose import jwt

from app.core.config import settings

"""
Логика токенов: создание и проверка JWT-токенов.
"""

async def create_token(
        response: Response,
        data: dict,
        type_token: str,
        expires_minutes: int,
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire, "type": type_token})
    token = jwt.encode(
        to_encode,
        settings.PRIVATE_KEY_PATH.read_text(),
        algorithm=settings.ALGORITHM
    )
    response.set_cookie(type_token, token, httponly=True, secure=False)
    return token

async def create_access_token(
        response: Response,
        data: dict,
) -> str:
    return await create_token(
        response=response,
        data=data,
        type_token=settings.COOKIE_ACCESS_TOKEN_KEY,
        expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

async def create_refresh_token(
        response: Response,
        data: dict,
) -> str:
    return await create_token(
        response=response,
        data=data,
        type_token=settings.COOKIE_REFRESH_TOKEN_KEY,
        expires_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
    )

def decode_token(
        token: str,
) -> dict | None:
    try:
        payload = jwt.decode(
            token,
            settings.PUBLIC_KEY_PATH.read_text(),
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except Exception:
        return None

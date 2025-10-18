from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

"""
Отвечает за подключение и конфигурацию базы данных PostgreSQL.
--определяет Base — базовый класс моделей SQLAlchemy.
--настраивает движок (engine) и подключается к БД.
--создаёт AsyncSession — фабрику сессий для работы с БД.
"""

class Base(DeclarativeBase):
    pass

engine = create_async_engine(
    url=settings.DATABASE_URL,
    poolclass=NullPool,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

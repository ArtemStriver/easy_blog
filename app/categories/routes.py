from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import get_current_user
from app.categories.crud import (get_all_categories,
                                 get_category_by_slug,
                                 create_new_category,
                                 update_category_by_id,
                                 delete_category_by_id)
from app.categories.schemas import CategoryOut, CategoryCreate, CategoryUpdate
from app.core.database import get_async_session
from app.posts.crud import get_posts_by_category_slug
from app.posts.schemas import PostBase
from app.users.utils import get_current_admin
from app.users.schemas import UserRead, ResponseSchema

"""
REST API маршруты для работы с категориями.
Реализует:
--GET / — список категорий (публичный)
--GET /{slug}/posts — список постов категорий (публичный)
--GET /{slug} — категория детально
--POST / — создать категорию
--PUT /{category_id} — изменить категорию
--DELETE /{category_id} — удалить категорию
"""

categories_router = APIRouter(prefix="/categories", tags=["Categories"])

@categories_router.get(
    "/",
    response_model=list[CategoryOut],
)
async def list_categories(
        _: Annotated[UserRead, Depends(get_current_user)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
) -> list[CategoryOut]:
    return await get_all_categories(db)

@categories_router.get(
    "/{slug}/posts",
    response_model=list[PostBase],
)
async def get_posts_by_category(
        _: Annotated[UserRead, Depends(get_current_user)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
        slug: str,
) -> list[PostBase]:
    return await get_posts_by_category_slug(db, slug)

@categories_router.get(
    "/{slug}",
    response_model=CategoryOut
)
async def get_category(
        _: Annotated[UserRead, Depends(get_current_admin)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
        slug: str,
):
    return await get_category_by_slug(db, slug)

@categories_router.post(
    "/",
    response_model=CategoryOut,
)
async def create_category(
        data: CategoryCreate,
        _: Annotated[UserRead, Depends(get_current_admin)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
) -> CategoryOut:
    return await create_new_category(db, data)

@categories_router.put(
    "/{category_id}",
    response_model=CategoryOut
)
async def update_category(
        category_id: int,
        data: CategoryUpdate,
        _: Annotated[UserRead, Depends(get_current_admin)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
) -> CategoryOut:
    return await update_category_by_id(db, category_id, data)

@categories_router.delete(
    "/{category_id}",
    response_model=ResponseSchema,
)
async def delete_category(
        category_id: int,
        _: Annotated[UserRead, Depends(get_current_admin)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
) -> ResponseSchema:
    return await delete_category_by_id(db, category_id)

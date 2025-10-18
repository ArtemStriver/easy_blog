from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import get_current_user
from app.core.database import get_async_session
from app.posts.crud import get_all_posts, get_post_by_slug, delete_post_by_id, update_post_by_id, create_new_post
from app.posts.schemas import PostOut, PostBase, PostCreate, PostUpdate
from app.users.utils import get_current_admin
from app.users.schemas import UserRead, ResponseSchema

"""
REST API маршруты для работы с постами.
Реализует:
--GET / — список постов (публичный)
--GET /{slug} — пост детально (публичный)
--POST / — создать пост
--PUT /{post_id} — изменить пост
--DELETE /{post_id} — удалить пост
"""

posts_router = APIRouter(prefix="/posts", tags=["Posts"])

@posts_router.get(
    "/",
    response_model=list[PostBase]
)
async def list_posts(
        _: Annotated[UserRead, Depends(get_current_user)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
) -> list[PostBase]:
    return await get_all_posts(db)

@posts_router.get(
    "/{slug}",
    response_model=PostOut
)
async def get_post(
        _: Annotated[UserRead, Depends(get_current_user)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
        slug: str,
) -> PostOut:
    return await get_post_by_slug(db, slug)

@posts_router.post(
    "/",
    response_model=PostOut,
)
async def create_post(
        post_data: PostCreate,
        admin: Annotated[UserRead, Depends(get_current_admin)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
) -> PostOut:
    return await create_new_post(db, admin.id, post_data)

@posts_router.put(
    "/{post_id}",
    response_model=PostOut
)
async def update_post(
        post_id: int,
        post_data: PostUpdate,
        admin: Annotated[UserRead, Depends(get_current_admin)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
) -> PostOut:
    return await update_post_by_id(db, post_id, admin.id, post_data)

@posts_router.delete(
    "/{post_id}",
    response_model=ResponseSchema,
)
async def delete_post(
        post_id: int,
        admin: Annotated[UserRead, Depends(get_current_admin)],
        db: Annotated[AsyncSession, Depends(get_async_session)],
) -> ResponseSchema:
    return await delete_post_by_id(db, post_id, admin.id)

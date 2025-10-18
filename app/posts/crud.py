from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from app.core.sanitizer import sanitize_html, html_to_text
from app.posts.models import Post
from app.posts.schemas import PostOut, PostBase, PostCreate, PostUpdate
from app.users.schemas import ResponseSchema

"""
Бизнес-логика взаимодействия с базой данных.
Содержит CRUD-функции для Post.
Изолирует работу с БД от маршрутов API.
"""

async def get_all_posts(
        db: AsyncSession
) -> list[PostBase]:
    result = await db.execute(select(Post))
    return result.scalars().all()

async def get_post_by_slug(
        db: AsyncSession,
        slug: str,
) -> PostOut:
    result = await db.execute(select(Post).where(Post.slug == slug))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

async def get_post_by_id(
        db: AsyncSession,
        post_id: int,
) -> PostOut:
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

async def get_posts_by_category_slug(
        db: AsyncSession,
        slug: str,
) -> list[PostBase]:
    result = await db.execute(select(Post).where(Post.slug == slug))
    return result.scalars().all()

async def create_new_post(
        db: AsyncSession,
        author_id: int,
        post_data: PostCreate,
) -> PostOut:
    sanitized = sanitize_html(post_data.content)
    preview = html_to_text(post_data.content, max_length=200)

    new_post = Post(
        title=post_data.title,
        content=post_data.content,
        sanitized_content=sanitized,
        slug=post_data.slug,
        preview=preview,
        author_id=author_id,
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

async def update_post_by_id(
        db: AsyncSession,
        post_id: int,
        user_id: int,
        data: PostUpdate,
) -> PostOut:
    post = await get_post_by_id(db, post_id)
    if post.author_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the author")

    if data.title:
        post.title = data.title
    if data.content:
        post.content = data.content
        post.sanitized_content = sanitize_html(data.content)
        post.preview = html_to_text(data.content)
        post.slug = data.slug

    await db.commit()
    await db.refresh(post)
    return post

async def delete_post_by_id(
        db: AsyncSession,
        post_id: int,
        user_id: int,
) -> ResponseSchema:
    post = await get_post_by_id(db, post_id)
    if post.author_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the author")

    stmt = delete(Post).where(Post.id == post_id)
    await db.execute(stmt)
    await db.commit()
    return ResponseSchema(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="post deleted",
    )

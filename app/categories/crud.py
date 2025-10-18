from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from app.categories.models import Category
from app.categories.schemas import CategoryOut, CategoryCreate, CategoryUpdate
from app.users.schemas import ResponseSchema

"""
Бизнес-логика взаимодействия с базой данных.
Содержит CRUD-функции для Category.
Изолирует работу с БД от маршрутов API.
"""

async def get_all_categories(
        db: AsyncSession
) -> list[CategoryOut]:
    result = await db.execute(select(Category))
    return result.scalars().all()

async def get_category_by_slug(
        db: AsyncSession,
        slug: str
) -> CategoryOut:
    result = await db.execute(select(Category).where(Category.slug == slug))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

async def get_category_by_id(
        db: AsyncSession,
        category_id: int
) -> CategoryOut:
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

async def create_new_category(
        db: AsyncSession,
        data: CategoryCreate
) -> CategoryOut:
    existing = await db.execute(
        select(Category).where(
            (Category.name == data.name) | (Category.slug == data.slug)
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")

    new_category = Category(**data.dict())
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category

async def update_category_by_id(
        db: AsyncSession,
        category_id: int,
        data: CategoryUpdate
) -> CategoryOut:
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(category, key, value)

    await db.commit()
    await db.refresh(category)
    return category

async def delete_category_by_id(
        db: AsyncSession,
        category_id: int,
) -> ResponseSchema:
    category = await get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    stmt = delete(Category).where(Category.id == category_id)
    await db.execute(stmt)
    await db.commit()
    return ResponseSchema(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="category deleted",
    )

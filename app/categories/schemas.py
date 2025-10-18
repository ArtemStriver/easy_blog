from pydantic import BaseModel, Field, ConfigDict

"""
Pydantic-схемы для валидации и сериализации данных категорий.
"""

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)
    description: str | None = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None

class CategoryOut(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

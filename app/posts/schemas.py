from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

"""
Pydantic-схемы для валидации и сериализации данных постов.
"""

class PostBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str
    slug: str

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    slug: str

class PostOut(PostBase):
    id: int
    sanitized_content: str
    author_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


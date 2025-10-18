from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

"""
ORM-модели для работы с базой данных.
Определяет структуру таблицы Post.
"""

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    sanitized_content = Column(Text, nullable=False)
    preview = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    category = relationship("Category", back_populates="posts")
    author = relationship("User")

from app.categories.models import Category #noqa
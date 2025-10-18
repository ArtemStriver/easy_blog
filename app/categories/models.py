from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base

"""
ORM-модели для работы с базой данных.
Определяет структуру таблицы Category.
"""

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    posts = relationship("Post", back_populates="category")

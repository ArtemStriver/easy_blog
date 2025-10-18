from sqlalchemy import Column, Integer, String, Enum, DateTime, func, LargeBinary
from sqlalchemy.orm import relationship

from app.core.database import Base
import enum

"""
ORM-модели для работы с базой данных.
Определяет структуру таблицы User.
"""

class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    posts = relationship("Post", back_populates="author", cascade="all, delete")
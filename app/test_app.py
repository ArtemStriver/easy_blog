from sqlalchemy import select
from datetime import datetime

from app.categories.models import Category
from app.core.database import async_session_maker
from app.core.sanitizer import sanitize_html
from app.core.security import hash_password
from app.posts.models import Post
from app.users.models import User, UserRole

"""
Заполнение базы данных тестовыми пользователями, постами и категориями 
для проверки работы функционала сервиса.
"""

async def load_test_data():
    async with async_session_maker() as session:
        users_count = await session.scalar(select(User).limit(1))
        if users_count:
            return

        admin = User(
            email="admin@example.com",
            hashed_password=hash_password("string"),
            role=UserRole.ADMIN,
        )
        user = User(
            email="user@example.com",
            hashed_password=hash_password("string"),
            role=UserRole.USER,
        )

        session.add_all([admin, user])
        await session.flush()

        cat1 = Category(name="Технологии",
                        slug="technology",
                        description="Новости технологий и обзоры гаджетов.")
        cat2 = Category(name="Путешествия",
                        slug="travel",
                        description="Советы, истории и маршруты для путешественников.")
        session.add_all([cat1, cat2])
        await session.flush()

        post1_context = ("<p>В версии <strong>Python 3.13</strong> появились интересные "
                         "улучшения производительности.</p>")
        post1 = Post(
            title="Что нового в Python 3.13",
            slug="python-3-13-new",
            content=post1_context,
            sanitized_content=sanitize_html(post1_context),
            preview="Обзор нововведений Python 3.13...",
            author_id=admin.id,
            category_id=cat1.id,
            created_at=datetime.utcnow()
        )
        post2_context = ("<p>В этой статье разберём, как создать <em>Dockerfile</em> "
                         "для FastAPI приложения.</p>")
        post2 = Post(
            title="Как собрать Docker-контейнер для FastAPI",
            slug="fastapi-docker",
            content=post2_context,
            sanitized_content=sanitize_html(post2_context),
            preview="Пошаговое руководство по сборке контейнера FastAPI...",
            author_id=user.id,
            category_id=cat2.id,
            created_at=datetime.utcnow()
        )

        post3_context = ("<p>Если вы любите путешествовать, "
                         "обязательно посетите эти 10 удивительных мест.</p>")
        post3 = Post(
            title="10 лучших мест для отдыха в Европе",
            slug="top-places-europe",
            content=post3_context,
            sanitized_content=sanitize_html(post3_context),
            preview="Подборка красивейших мест Европы для вашего отпуска...",
            author_id=user.id,
            category_id=cat2.id,
            created_at=datetime.utcnow()
        )

        session.add_all([post1, post2, post3])
        await session.commit()

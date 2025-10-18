from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware

from app.auth.routes import auth_router
from app.categories.routes import categories_router
from app.posts.routes import posts_router
from app.test_app import load_test_data
from app.users.routes import users_router

"""
Главная точка входа в приложение FastAPI.
--инициализирует приложение, origins и  middleware
--создает тестовые данные для проверки приложения через swagger
--подключает маршруты (routers)
"""

app = FastAPI(
    title="FastAPI Blog Backend",
    docs_url="/docs",
)

@app.on_event("startup")
async def startup_event():
    await load_test_data()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(auth_router)
main_router.include_router(users_router)
main_router.include_router(posts_router)
main_router.include_router(categories_router)

app.include_router(main_router)

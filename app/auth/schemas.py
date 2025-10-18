from pydantic import BaseModel

"""
Pydantic-схемы для валидации и сериализации данных авторизации.
"""

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

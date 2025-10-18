from fastapi import Depends, HTTPException

from app.auth.utils import get_current_user
from app.users.models import User

"""
Вспомогательные функции и утилиты.
Содержит функцию проверки пользователя на роль админа.
"""

def get_current_admin(
        current_user: User = Depends(get_current_user)
):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
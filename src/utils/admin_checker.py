from fastapi import Depends, HTTPException, status
from src.services.auth import get_current_user


class AdminChecker:
    """
        Показывает, является ли текущий авторизованный пользователь админом.
    """

    def __call__(self, user_info: dict = Depends(get_current_user)):
        is_admin = user_info.get('is_admin')

        if not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Недостаточно прав',
            )

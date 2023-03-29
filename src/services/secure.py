from passlib.handlers.pbkdf2 import pbkdf2_sha256
from src.core.settings import settings


class SecureService:
    @staticmethod
    async def hash_password(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    @staticmethod
    async def verify_password(password_text: str, password_hash: str) -> bool:
        return pbkdf2_sha256.verify(password_text, password_hash)

    @staticmethod
    async def is_admin_user(user_login: str) -> bool:
        return user_login == settings.admin_login

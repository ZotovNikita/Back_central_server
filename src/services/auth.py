from typing import Optional
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.core.settings import settings
from src.repositories.users import UsersRepository
from src.models.schemas.utils.jwt_token import JwtToken
from src.services.secure import SecureService


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_current_user(token: str = Depends(oauth2_schema)) -> dict:
    return await AuthService.decode_token(token)


class AuthService:
    def __init__(self, users_repository: UsersRepository = Depends()):
        self.users_repo = users_repository

    @staticmethod
    async def encode_token(user_guid: str, user_login: str) -> JwtToken:
        now = datetime.now(timezone.utc)
        payload = {
            'iat': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_seconds),
            'user_guid': str(user_guid),
            'is_admin': await SecureService.is_admin_user(user_login)
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return JwtToken(access_token=token)

    @staticmethod
    async def decode_token(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Некорректный токен')
        return {
            'user_guid': payload.get('user_guid'),
            'is_admin': payload.get('is_admin')
        }

    @staticmethod
    async def is_valid_token(token: str) -> bool:
        try:
            jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            return False
        return True

    async def login(self, login: str, password_text: str) -> Optional[JwtToken]:
        if not (user := await self.users_repo.get_by_login(login)):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if not await SecureService.verify_password(password_text, user.password_hashed):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return await self.encode_token(user.guid, user.login)

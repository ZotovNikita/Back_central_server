from typing import Optional
from fastapi import HTTPException, status
from jose import JWTError, jwt
from src.core.settings import settings
from src.models.schemas.utils.jwt_token import JwtToken


class AuthorizationService:
    @staticmethod
    def create_token(guid: str) -> JwtToken:
        payload = {
            'guid': guid,
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return JwtToken(access_token=token)

    @staticmethod
    def verify_token(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Некорректный токен')
        return payload
    
    @staticmethod
    def verify_guid(guid: str) -> bool:
        return True  # todo: запрос в бд
    
    def authorize(self, guid: str) -> JwtToken:
        if not self.verify_guid(guid):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return self.create_token(guid)

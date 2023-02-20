from typing import Optional
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.core.settings import settings
from src.models.users import Users
from src.models.schemas.auth.auth_request import AuthRequest
from src.models.schemas.utils.jwt_token import JwtToken


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')


def get_current_user(token: str = Depends(oauth2_schema)) -> dict:
    return AuthService.decode_token(token)


class AuthService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_password(password_text: str, password_hash: str) -> bool:
        return pbkdf2_sha256.verify(password_text, password_hash)

    @staticmethod
    def encode_token(user_guid: str) -> JwtToken:
        now = datetime.now(timezone.utc)
        payload = {
            'iat': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_seconds),
            'user_guid': str(user_guid)
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return JwtToken(access_token=token)

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Некорректный токен')
        return payload.get('user_guid')
    
    def register(self, auth_request: AuthRequest) -> None:
        is_exist = (
            self.session
            .query(Users)
            .filter(Users.login == auth_request.login)
            .count()
        )
        if is_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)
        
        user = Users(
            login=auth_request.login,
            password_hashed=self.hash_password(auth_request.password_text)
        )
        self.session.add(user)
        self.session.commit()
    
    def login(self, login: str, password_text: str) -> Optional[JwtToken]:
        user = (
            self.session
            .query(Users)
            .filter(Users.login == login)
            .first()
        )
        
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if not self.verify_password(password_text, user.password_hashed):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        
        return self.encode_token(user.guid)

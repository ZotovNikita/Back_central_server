from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.models.schemas.utils.jwt_token import JwtToken
from src.services.auth import AuthService


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/login', response_model=JwtToken, name='Авторизация пользователя')
def login(auth_schema: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends()) -> JwtToken:
    return service.login(auth_schema.username, auth_schema.password)

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.models.schemas.utils.jwt_token import JwtToken
from src.services.auth import AuthService
from src.models.schemas.auth.auth_request import AuthRequest


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/login', response_model=JwtToken, name='Авторизация пользователя')
def login(auth_schema: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends()) -> JwtToken:
    return service.login(auth_schema.username, auth_schema.password)


@router.post('/register', status_code=status.HTTP_201_CREATED, name='Регистрация пользователя')
def register(auth_schema: AuthRequest, service: AuthService = Depends()):
    return service.register(auth_schema)

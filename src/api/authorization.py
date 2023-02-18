from fastapi import APIRouter, Depends
from src.models.schemas.authorization.authorization_request import AuthorizationRequest
from src.models.schemas.utils.jwt_token import JwtToken
from src.services.authorization import AuthorizationService


router = APIRouter(
    prefix='/authorize',
    tags=['authorize'],
)


@router.post('/guid', response_model=JwtToken, name='Авторизация пользователя')
def authorize(schema: AuthorizationRequest, service: AuthorizationService = Depends()) -> JwtToken:
    return service.authorize(schema.guid)

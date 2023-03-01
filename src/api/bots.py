from typing import List
from fastapi import APIRouter, status, Depends
from pydantic import UUID4
from src.services.auth import get_current_user
from src.services.bots import BotsService
from src.models.schemas.bots.bots_request import BotsRequest
from src.models.schemas.bots.bots_response import BotsResponse, BotsAllowedResponse
from src.models.schemas.bot_data.bot_data_request import BotDataRequest
from src.models.schemas.bot_data.bot_data_response import BotDataResponse
from src.api.utils.admin_checker import IS_ADMIN


router = APIRouter(
    prefix='/bots',
    tags=['bots'],
    dependencies=[Depends(get_current_user)],
)


@router.get('/{guid}', response_model=BotsResponse, name='Получить бота', dependencies=[Depends(IS_ADMIN)])
def get(guid: UUID4, service: BotsService = Depends()):
    return service.get(guid)


@router.get('/', response_model=List[BotsResponse], name='Получить всех ботов', dependencies=[Depends(IS_ADMIN)])
def all(service: BotsService = Depends()):
    return service.all()


@router.post('/', response_model=BotsResponse, status_code=status.HTTP_201_CREATED, name='Добавить бота', dependencies=[Depends(IS_ADMIN)])
def add(request: BotsRequest, service: BotsService = Depends()):
    return service.add(request)


@router.post('/{guid}', response_model=BotsResponse, name='Изменить бота', dependencies=[Depends(IS_ADMIN)])
def update(guid: UUID4, request: BotsRequest, service: BotsService = Depends()):
    return service.update(guid, request)


@router.delete('/{guid}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить бота', dependencies=[Depends(IS_ADMIN)])
def delete(guid: UUID4, service: BotsService = Depends()):
    return service.delete(guid)


@router.get('/allowed/', response_model=List[BotsAllowedResponse], name='Получить доступных пользователю ботов')
def get(current_user: dict = Depends(get_current_user), service: BotsService = Depends()):
    return service.allowed_bots_for_user(current_user)


@router.get('/intents/{bot_guid}', name='Тест получения интентов')
def get(bot_guid: UUID4):
    print(bot_guid)
    data = {f'Intent {i}': f'Что-то {i}' for i in range(30)}
    return data


# ! переместить?
@router.post('/predict', response_model=BotDataResponse, name='Тест запроса от ботов')
def predict(request: BotDataRequest):
    msg = 'Done_' + request.message
    return {'message': msg}

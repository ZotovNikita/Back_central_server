from typing import List
from fastapi import APIRouter, status, Depends
from pydantic import UUID4
from src.services.bots import BotsService
from src.models.schemas.bots.bots_request import BotsRequest
from src.models.schemas.bots.bots_response import BotsResponse
from src.dependencies import AUTHORIZED, ADMIN_ONLY


router = APIRouter(
    prefix='/bots',
    tags=['bots'],
    dependencies=[Depends(AUTHORIZED)],
)


@router.get('/{guid}', response_model=BotsResponse, name='Получить бота', dependencies=[Depends(ADMIN_ONLY)])
def get(guid: UUID4, service: BotsService = Depends()):
    return service.get(guid)


@router.get('/', response_model=List[BotsResponse], name='Получить всех ботов', dependencies=[Depends(ADMIN_ONLY)])
def all(service: BotsService = Depends()):
    return service.all()


@router.post('/', response_model=BotsResponse, status_code=status.HTTP_201_CREATED, name='Добавить бота', dependencies=[Depends(ADMIN_ONLY)])
def add(request: BotsRequest, service: BotsService = Depends()):
    return service.add(request)


@router.post('/{guid}', response_model=BotsResponse, name='Изменить бота', dependencies=[Depends(ADMIN_ONLY)])
def update(guid: UUID4, request: BotsRequest, service: BotsService = Depends()):
    return service.update(guid, request)


@router.delete('/{guid}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить бота', dependencies=[Depends(ADMIN_ONLY)])
def delete(guid: UUID4, service: BotsService = Depends()):
    return service.delete(guid)


@router.get('/allowed/', response_model=List[BotsResponse], name='Получить доступных пользователю ботов')
def get(current_user: dict = Depends(AUTHORIZED), service: BotsService = Depends()):
    return service.allowed_bots_for_user(current_user)

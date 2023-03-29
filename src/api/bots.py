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
async def get_by_guid(guid: UUID4, service: BotsService = Depends()):
    return await service.get_by_guid(guid)


@router.get('/', response_model=List[BotsResponse], name='Получить всех ботов', dependencies=[Depends(ADMIN_ONLY)])
async def get_all(service: BotsService = Depends()):
    return await service.get_all()


@router.post('/', response_model=BotsResponse, status_code=status.HTTP_201_CREATED, name='Добавить бота', dependencies=[Depends(ADMIN_ONLY)])
async def add(request: BotsRequest, service: BotsService = Depends()):
    return await service.add(request)


@router.post('/{guid}', response_model=BotsResponse, name='Изменить бота', dependencies=[Depends(ADMIN_ONLY)])
async def update_by_guid(guid: UUID4, request: BotsRequest, service: BotsService = Depends()):
    bot = await service.get_by_guid(guid)
    return await service.update(bot, request)


@router.delete('/{guid}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить бота', dependencies=[Depends(ADMIN_ONLY)])
async def delete_by_guid(guid: UUID4, service: BotsService = Depends()):
    bot = await service.get_by_guid(guid)
    return await service.delete(bot)


@router.get('/allowed/', response_model=List[BotsResponse], name='Получить доступных пользователю ботов')
async def get_all_allowed_user(current_user: dict = Depends(AUTHORIZED), service: BotsService = Depends()):
    return await service.get_all_by_user_guid(current_user)

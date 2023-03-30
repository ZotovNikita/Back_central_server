from typing import List
from pydantic import UUID4
from fastapi import APIRouter, status, Depends
from src.services.relations import RelationsService
from src.models.schemas.relations.request import RelationsRequestDB
from src.models.schemas.relations.response import RelationsResponse
from src.dependencies import ADMIN_ONLY


router = APIRouter(
    prefix='/relations',
    tags=['relations'],
    dependencies=[Depends(ADMIN_ONLY)],
)


@router.get('/{id}', response_model=RelationsResponse, name='Получить связь по id')
async def get_by_id(id: int, service: RelationsService = Depends()):
    return await service.get_by_id(id)


@router.get('/', response_model=List[RelationsResponse], name='Получить все связи')
async def get_all(service: RelationsService = Depends()):
    return await service.get_all()


@router.post('/', response_model=RelationsResponse, status_code=status.HTTP_201_CREATED,
             name='Добавить связь по guid пользователя и бота')
async def add_by_user_guid_and_bot_guid(request: RelationsRequestDB, service: RelationsService = Depends()):
    return await service.add_by_user_guid_and_bot_guid(request)


@router.post('/{user_guid}/{bot_guid}', response_model=RelationsResponse, name='Изменить связь по guid пользователя и бота')
async def update_by_user_guid_and_bot_guid(user_guid: UUID4, bot_guid: UUID4, request: RelationsRequestDB, service: RelationsService = Depends()):
    relation = await service.get_by_user_guid_and_bot_guid(user_guid, bot_guid)
    return await service.update(relation, request)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить связь по id')
async def delete(id: int, service: RelationsService = Depends()):
    relation = await service.get_by_id(id)
    return await service.delete(relation)


@router.delete('/{user_guid}/{bot_guid}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить связь по guid пользователя и бота')
async def delete(user_guid: UUID4, bot_guid: UUID4, service: RelationsService = Depends()):
    relation = await service.get_by_user_guid_and_bot_guid(user_guid, bot_guid)
    return await service.delete(relation)

from typing import List
from pydantic import UUID4
from fastapi import APIRouter, status, Depends
from src.services.intents import IntentsService
from src.models.schemas.intents.intents_request import IntentsRequestForm, IntentsRequestDB
from src.models.schemas.intents.intents_response import IntentsResponse
from src.dependencies import AUTHORIZED, ADMIN_ONLY


router = APIRouter(
    prefix='/intents',
    tags=['intents'],
    dependencies=[Depends(AUTHORIZED)],
)


@router.get('/w/{id}', response_model=IntentsResponse, name='(!) Получить интент по id', dependencies=[Depends(ADMIN_ONLY)])
async def get_by_id(id: int, service: IntentsService = Depends()):
    return await service.get_by_id(id)


@router.get('/w', response_model=List[IntentsResponse], name='(!) Получить все интенты', dependencies=[Depends(ADMIN_ONLY)])
async def get_all(service: IntentsService = Depends()):
    return await service.get_all()


@router.post('/w/{id}', response_model=IntentsResponse, name='(!) Изменить интент по id', dependencies=[Depends(ADMIN_ONLY)])
async def update_by_id(id: int, request: IntentsRequestForm, service: IntentsService = Depends()):
    intent = await service.get_by_id(id)
    return await service.update(intent, request)


@router.delete('/w/{id}', status_code=status.HTTP_204_NO_CONTENT, name='(!) Удалить интент по id', dependencies=[Depends(ADMIN_ONLY)])
async def delete_by_id(id: int, service: IntentsService = Depends()):
    intent = await service.get_by_id(id)
    return await service.delete(intent)


@router.get('/allowed/{bot_guid}', response_model=List[IntentsResponse], name='Получить все интенты бота')
async def get_all_by_bot_guid(bot_guid: UUID4, service: IntentsService = Depends()):
    return await service.get_all_by_bot_guid(bot_guid)


@router.post('/form', response_model=IntentsResponse, status_code=status.HTTP_201_CREATED, name='Добавить интент по форме')
async def add_by_form(request: IntentsRequestForm, service: IntentsService = Depends(), user: dict = Depends(AUTHORIZED)):
    # ! по request.examples обучить модель ?
    return await service.add(request, user)


@router.post('/form/{bot_guid}/{name}', response_model=IntentsResponse, name='Изменить интент по форме')
async def update_by_form(bot_guid: UUID4, name: str, request: IntentsRequestForm, service: IntentsService = Depends()):
    # ! по request.examples переобучить модель ?
    intent = await service.get_by_bot_guid_and_name(bot_guid, name)
    return await service.update(intent, request)


@router.delete('/form/{bot_guid}/{name}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить интент по форме')
async def delete_by_bot_guid_and_name(bot_guid: UUID4, name: str, service: IntentsService = Depends()):
    # ! что-то происходит в модели ?
    intent = await service.get_by_bot_guid_and_name(bot_guid, name)
    return await service.delete(intent)

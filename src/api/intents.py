from typing import List
from fastapi import APIRouter, status, Depends
from pydantic import UUID4
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
async def get(id: int, service: IntentsService = Depends()):
    return await service.get(id)


@router.get('/w', response_model=List[IntentsResponse], name='(!) Получить все интенты', dependencies=[Depends(ADMIN_ONLY)])
async def all(service: IntentsService = Depends()):
    return await service.all()


@router.post('/w', response_model=IntentsResponse, status_code=status.HTTP_201_CREATED, name='(!) Добавить интент', dependencies=[Depends(ADMIN_ONLY)])
async def add(request: IntentsRequestDB, service: IntentsService = Depends(), user: dict = Depends(AUTHORIZED)):
    return await service.add(request, user)


@router.post('/w/{id}', response_model=IntentsResponse, name='(!) Изменить интент', dependencies=[Depends(ADMIN_ONLY)])
async def update(id: int, request: IntentsRequestDB, service: IntentsService = Depends()):
    return await service.update(id, request)


@router.delete('/w/{id}', status_code=status.HTTP_204_NO_CONTENT, name='(!) Удалить интент', dependencies=[Depends(ADMIN_ONLY)])
async def delete(id: int, service: IntentsService = Depends()):
    return await service.delete(id)


@router.get('/allowed/{bot_guid}', response_model=List[IntentsResponse], name='Получить все интенты бота')
async def get(bot_guid: UUID4, service: IntentsService = Depends()):
    return await service.all_intents_for_bot(bot_guid)


@router.post('/form', response_model=IntentsResponse, status_code=status.HTTP_201_CREATED, name='Добавить интент по форме')
async def add(request: IntentsRequestForm, service: IntentsService = Depends(), user: dict = Depends(AUTHORIZED)):
    # ! по request.examples обучить модель ?
    return await service.add(request, user)


@router.post('/form/{bot_guid}/{name}', response_model=IntentsResponse, name='Изменить интент по форме')
async def update(bot_guid: UUID4, name: str, request: IntentsRequestForm, service: IntentsService = Depends()):
    # ! по request.examples переобучить модель ?
    return await service.update_by_bot_guid_and_name(bot_guid, name, request)


@router.delete('/form/{bot_guid}/{name}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить интент по форме')
async def delete(bot_guid: UUID4, name: str, service: IntentsService = Depends()):
    # ! что-то происходит в модели ?
    return await service.delete_by_bot_guid_and_name(bot_guid, name)

from typing import List
from fastapi import APIRouter, status, Depends
from pydantic import UUID4
from src.api.utils.admin_checker import IS_ADMIN
from src.services.auth import get_current_user
from src.services.intents import IntentsService
from src.models.schemas.intents.intents_request import IntentsRequestForm, IntentsRequestDB
from src.models.schemas.intents.intents_response import IntentsResponse


router = APIRouter(
    prefix='/intents',
    tags=['intents'],
    dependencies=[Depends(get_current_user)],
)


@router.get('/w/{id}', response_model=IntentsResponse, name='(!) Получить интент по id', dependencies=[Depends(IS_ADMIN)])
def get(id: int, service: IntentsService = Depends()):
    return service.get(id)


@router.get('/w', response_model=List[IntentsResponse], name='(!) Получить все интенты', dependencies=[Depends(IS_ADMIN)])
def all(service: IntentsService = Depends()):
    return service.all()


@router.post('/w', response_model=IntentsResponse, status_code=status.HTTP_201_CREATED, name='(!) Добавить интент', dependencies=[Depends(IS_ADMIN)])
def add(request: IntentsRequestDB, service: IntentsService = Depends(), user: dict = Depends(get_current_user)):
    return service.add(request, user)


@router.post('/w/{id}', response_model=IntentsResponse, name='(!) Изменить интент', dependencies=[Depends(IS_ADMIN)])
def update(id: int, request: IntentsRequestDB, service: IntentsService = Depends()):
    return service.update(id, request)


@router.delete('/w/{id}', status_code=status.HTTP_204_NO_CONTENT, name='(!) Удалить интент', dependencies=[Depends(IS_ADMIN)])
def delete(id: int, service: IntentsService = Depends()):
    return service.delete(id)


@router.get('/allowed/{bot_guid}', response_model=List[IntentsResponse], name='Получить все интенты бота')
def get(bot_guid: UUID4, service: IntentsService = Depends()):
    return service.all_intents_for_bot(bot_guid)


@router.post('/form', response_model=IntentsResponse, status_code=status.HTTP_201_CREATED, name='Добавить интент по форме')
def add(request: IntentsRequestForm, service: IntentsService = Depends(), user: dict = Depends(get_current_user)):
    # ! по request.examples обучить модель ?
    return service.add(request, user)


@router.post('/form/{bot_guid}/{name}', response_model=IntentsResponse, name='Изменить интент по форме')
def update(bot_guid: UUID4, name: str, request: IntentsRequestForm, service: IntentsService = Depends()):
    # ! по request.examples переобучить модель ?
    return service.update_by_bot_guid_and_name(bot_guid, name, request)


@router.delete('/form/{bot_guid}/{name}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить интент по форме')
def delete(bot_guid: UUID4, name: str, service: IntentsService = Depends()):
    # ! что-то происходит в модели ?
    return service.delete_by_bot_guid_and_name(bot_guid, name)

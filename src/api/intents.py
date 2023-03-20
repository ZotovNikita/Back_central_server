from typing import List
from fastapi import APIRouter, status, Depends
from pydantic import UUID4
from src.api.utils.admin_checker import IS_ADMIN
from src.services.auth import get_current_user
from src.services.intents import IntentsService
from src.models.schemas.intents.intents_request import IntentsRequest, IntentsRequestAdmin
from src.models.schemas.intents.intents_response import IntentsResponse


router = APIRouter(
    prefix='/intents',
    tags=['intents'],
    dependencies=[Depends(get_current_user)],
)


@router.get('/{id}', response_model=IntentsResponse, name='Получить интент по id', dependencies=[Depends(IS_ADMIN)])
def get(id: int, service: IntentsService = Depends()):
    return service.get(id)


@router.get('/', response_model=List[IntentsResponse], name='Получить все интенты', dependencies=[Depends(IS_ADMIN)])
def all(service: IntentsService = Depends()):
    return service.all()


@router.post('/', response_model=IntentsResponse, status_code=status.HTTP_201_CREATED, name='Добавить интент (warning)', dependencies=[Depends(IS_ADMIN)])
def add(request: IntentsRequestAdmin, service: IntentsService = Depends(), user: dict = Depends(get_current_user)):
    return service.add(request, user)


@router.post('/{id}', response_model=IntentsResponse, name='Изменить интент (warning)', dependencies=[Depends(IS_ADMIN)])
def update(id: int, request: IntentsRequestAdmin, service: IntentsService = Depends()):
    return service.update(id, request)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить интент (warning)', dependencies=[Depends(IS_ADMIN)])
def delete(id: int, service: IntentsService = Depends()):
    return service.delete(id)


@router.get('/{bot_guid}', response_model=List[IntentsResponse], name='Получить все интенты бота')
def get(bot_guid: UUID4, service: IntentsService = Depends()):
    return service.all_intents_for_bot(bot_guid)

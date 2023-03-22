from typing import List
from fastapi import APIRouter, status, Depends
from pydantic import UUID4
from src.api.utils.admin_checker import IS_ADMIN
from src.services.auth import get_current_user
from src.services.intents import IntentsService
from src.models.schemas.intents.intents_request import IntentsRequest
from src.models.schemas.intents.intents_response import IntentsResponse


router = APIRouter(
    prefix='/intent_generator',
    tags=['intent_generator'],
    dependencies=[Depends(get_current_user)],
)


@router.post('/', response_model=IntentsResponse, status_code=status.HTTP_201_CREATED, name='Добавить интент')
def add(request: IntentsRequest, service: IntentsService = Depends(), user: dict = Depends(get_current_user)):
    #передать в фит
    return service.add(request, user)


@router.post('/{id}', response_model=IntentsResponse, name='Изменить интент')
def update(id: int, request: IntentsRequest, service: IntentsService = Depends()):
    #передать в фит
    return service.update(id, request)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить интент')
def delete(id: int, service: IntentsService = Depends()):
    #передать в фит
    return service.delete(id)

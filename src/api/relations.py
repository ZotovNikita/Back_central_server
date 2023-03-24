from typing import List
from fastapi import APIRouter, status, Depends
from src.services.relations import RelationsService
from src.models.schemas.relations.request import RelationsRequest
from src.models.schemas.relations.response import RelationsResponse
from src.dependencies import ADMIN_ONLY


router = APIRouter(
    prefix='/relations',
    tags=['relations'],
    dependencies=[Depends(ADMIN_ONLY)],
)


@router.get('/{id}', response_model=RelationsResponse, name='Получить связь по id')
def get(id: int, service: RelationsService = Depends()):
    return service.get(id)


@router.get('/', response_model=List[RelationsResponse], name='Получить все связи')
def all(service: RelationsService = Depends()):
    return service.all()


@router.post('/', response_model=RelationsResponse, status_code=status.HTTP_201_CREATED, name='Добавить связь')
def add(request: RelationsRequest, service: RelationsService = Depends()):
    return service.add(request)


@router.post('/{id}', response_model=RelationsResponse, name='Изменить связь')
def update(id: int, request: RelationsRequest, service: RelationsService = Depends()):
    return service.update(id, request)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить связь')
def delete(id: int, service: RelationsService = Depends()):
    return service.delete(id)

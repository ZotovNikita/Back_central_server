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
async def get(id: int, service: RelationsService = Depends()):
    return await service.get(id)


@router.get('/', response_model=List[RelationsResponse], name='Получить все связи')
async def all(service: RelationsService = Depends()):
    return await service.all()


@router.post('/', response_model=RelationsResponse, status_code=status.HTTP_201_CREATED, name='Добавить связь')
async def add(request: RelationsRequest, service: RelationsService = Depends()):
    return await service.add(request)


@router.post('/{id}', response_model=RelationsResponse, name='Изменить связь')
async def update(id: int, request: RelationsRequest, service: RelationsService = Depends()):
    return await service.update(id, request)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить связь')
async def delete(id: int, service: RelationsService = Depends()):
    return await service.delete(id)

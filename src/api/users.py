from typing import List
from fastapi import APIRouter, status, Depends
from pydantic import UUID4
from src.services.users import UsersService
from src.models.schemas.users.users_request import UsersRequest
from src.models.schemas.users.users_response import UsersResponse
from src.dependencies import ADMIN_ONLY


router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(ADMIN_ONLY)]
)


@router.get('/{guid}', response_model=UsersResponse, name='Получить пользователя')
async def get(guid: UUID4, service: UsersService = Depends()):
    return await service.get(guid)


@router.get('/', response_model=List[UsersResponse], name='Получить всех пользователей')
async def all(service: UsersService = Depends()):
    return await service.all()


@router.post('/', response_model=UsersResponse, status_code=status.HTTP_201_CREATED, name='Регистрация пользователя')
async def register(request: UsersRequest, service: UsersService = Depends()):
    return await service.add(request)


@router.post('/{guid}', response_model=UsersResponse, name='Изменить пользователя')
async def update(guid: UUID4, request: UsersRequest, service: UsersService = Depends()):
    return await service.update(guid, request)


@router.delete('/{guid}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить пользователя')
async def delete(guid: UUID4, service: UsersService = Depends()):
    return await service.delete(guid)

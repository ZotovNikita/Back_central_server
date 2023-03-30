from typing import List
from fastapi import APIRouter, status, Depends
from pydantic import UUID4
from src.services.users import UsersService
from src.models.schemas.users.request import UsersRequest
from src.models.schemas.users.response import UsersResponse
from src.dependencies import ADMIN_ONLY


router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(ADMIN_ONLY)]
)


@router.get('/{guid}', response_model=UsersResponse, name='Получить пользователя по guid')
async def get_by_guid(guid: UUID4, service: UsersService = Depends()):
    return await service.get_by_guid(guid)


@router.get('/', response_model=List[UsersResponse], name='Получить всех пользователей')
async def get_all(service: UsersService = Depends()):
    return await service.get_all()


@router.post('/', response_model=UsersResponse, status_code=status.HTTP_201_CREATED, name='Регистрация пользователя')
async def register(request: UsersRequest, service: UsersService = Depends()):
    return await service.add(request)


@router.post('/{guid}', response_model=UsersResponse, name='Изменить пользователя по guid')
async def update_by_guid(guid: UUID4, request: UsersRequest, service: UsersService = Depends()):
    user = await service.get_by_guid(guid)
    return await service.update(user, request)


@router.delete('/{guid}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить пользователя по guid')
async def delete_by_guid(guid: UUID4, service: UsersService = Depends()):
    user = await service.get_by_guid(guid)
    return await service.delete(user)

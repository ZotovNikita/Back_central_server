from typing import List
from fastapi import APIRouter, status, Depends
from pydantic import UUID4
from src.api.utils.admin_checker import IS_ADMIN
from src.services.users import UsersService
from src.models.schemas.users.users_request import UsersRequest
from src.models.schemas.users.users_response import UsersResponse


router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(IS_ADMIN)]
)


@router.get('/{guid}', response_model=UsersResponse, name='Получить пользователя')
def get(guid: UUID4, service: UsersService = Depends()):
    return service.get(guid)


@router.get('/', response_model=List[UsersResponse], name='Получить всех пользователей')
def all(service: UsersService = Depends()):
    return service.all()


@router.post('/', response_model=UsersResponse, status_code=status.HTTP_201_CREATED, name='Регистрация пользователя')
def register(request: UsersRequest, service: UsersService = Depends()):
    return service.add(request)


@router.post('/{guid}', response_model=UsersResponse, name='Изменить пользователя')
def update(guid: UUID4, request: UsersRequest, service: UsersService = Depends()):
    return service.update(guid, request)


@router.delete('/{guid}', status_code=status.HTTP_204_NO_CONTENT, name='Удалить пользователя')
def delete(guid: UUID4, service: UsersService = Depends()):
    return service.delete(guid)

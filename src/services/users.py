from typing import List
from fastapi import HTTPException, status, Depends
from src.repositories.users import UsersRepository
from src.models.users import Users
from src.models.schemas.users.request import UsersRequest, UsersRequestDB
from src.services.secure import SecureService


class UsersService:
    def __init__(self, repository: UsersRepository = Depends(), secure_service: SecureService = Depends()):
        self.repo = repository
        self.secure_service = secure_service

    async def get_all(self) -> List[Users]:
        return await self.repo.get_all()

    async def get_by_guid(self, guid: str) -> Users:
        if not (user := await self.repo.get_by_guid(guid)):
            raise HTTPException(status_code=404,
                                detail='Пользователь не найден')
        return user

    async def add(self, request: UsersRequest) -> Users:
        if await self.repo.get_by_login(request.login):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Пользователь с таким логином уже существует')
        return await self.repo.add(
            UsersRequestDB(**dict(request), password_hashed=await self.secure_service.hash_password(request.password_text))
        )

    async def update(self, user: Users, request: UsersRequest) -> Users:
        same_user = await self.repo.get_by_login(request.login)

        if same_user and user.guid != same_user.guid:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Пользователь с таким логином уже существует')

        return await self.repo.update(
            user,
            UsersRequestDB(**dict(request), password_hashed=await self.secure_service.hash_password(request.password_text))
        )

    async def delete(self, user: Users) -> None:
        await self.repo.delete(user)

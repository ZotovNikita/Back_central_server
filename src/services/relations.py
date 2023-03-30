from typing import List
from fastapi import HTTPException, status, Depends
from src.repositories.relations import RelationsRepository
from src.models.relations import Relations
from src.models.schemas.relations.request import RelationsRequestDB
from src.services.users import UsersService
from src.services.bots import BotsService


class RelationsService:
    def __init__(self, repository: RelationsRepository = Depends(), users_service: UsersService = Depends(), bots_service: BotsService = Depends()):
        self.repo = repository
        self.users_service = users_service
        self.bots_service = bots_service

    async def get_all(self) -> List[Relations]:
        return await self.repo.get_all()

    async def get_by_id(self, id: int) -> Relations:
        if not (relation := await self.repo.get_by_id(id)):
            raise HTTPException(status_code=404, detail='Связь не найдена')
        return relation

    async def get_by_user_guid_and_bot_guid(self, user_guid: str, bot_guid: str) -> Relations:
        if not (relation := await self.repo.get_by_user_guid_and_bot_guid(user_guid, bot_guid)):
            raise HTTPException(status_code=404, detail='Связь не найдена')
        return relation

    async def add_by_user_guid_and_bot_guid(self, request: RelationsRequestDB) -> Relations:
        user = await self.users_service.get_by_guid(request.user_guid)
        bot = await self.bots_service.get_by_guid(request.bot_guid)

        if await self.repo.get_by_user_guid_and_bot_guid(user.guid, bot.guid):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Такая связь уже существует')

        return await self.repo.add(request)

    async def update(self, relation: Relations, request: RelationsRequestDB) -> Relations:
        same_relation = await self.repo.get_by_user_guid_and_bot_guid(request.user_guid, request.bot_guid)

        if same_relation and relation.id != same_relation.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Полученные данные вызвали конфликт с существующей связью')

        return await self.repo.update(relation, request)

    async def delete(self, relation: Relations) -> None:
        await self.repo.delete(relation)

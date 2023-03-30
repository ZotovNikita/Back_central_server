from typing import List
from fastapi import HTTPException, status, Depends
from src.repositories.bots import BotsRepository
from src.models.bots import Bots
from src.models.schemas.bots.request import BotsRequest


class BotsService:
    def __init__(self, repository: BotsRepository = Depends()):
        self.repo = repository

    async def get_all(self) -> List[Bots]:
        return await self.repo.get_all()

    async def get_all_by_user_guid(self, user: dict) -> List[Bots]:
        return await self.repo.get_all_by_user_guid(user.get('user_guid'))

    async def get_by_guid(self, guid: str) -> Bots:
        if not (bot := await self.repo.get_by_guid(guid)):
            raise HTTPException(status_code=404, detail='Бот не найден')
        return bot

    async def add(self, request: BotsRequest) -> Bots:
        if await self.repo.get_by_guid(request.guid):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Полученные данные конфликтуют с существующим ботом')
        return await self.repo.add(request)

    async def update(self, bot: Bots, request: BotsRequest) -> Bots:
        same_bot = await self.repo.get_by_guid(request.guid)

        if same_bot and bot.guid != same_bot.guid:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Полученные данные конфликтуют с существующим ботом')

        return await self.repo.update(bot, request)

    async def delete(self, bot: Bots) -> None:
        await self.repo.delete(bot)

from typing import List
from fastapi import HTTPException, status, Depends
from src.repositories.intents import IntentsRepository
from src.models.intents import Intents
from src.models.schemas.intents.intents_request import IntentsRequestDB


class IntentsService:
    def __init__(self, repository: IntentsRepository = Depends()):
        self.repo = repository

    async def get_all(self) -> List[Intents]:
        return await self.repo.get_all()

    async def get_all_by_bot_guid(self, bot_guid: str) -> List[Intents]:
        return await self.repo.get_all_by_bot_guid(bot_guid)

    async def get_by_id(self, id: int) -> Intents:
        if not (intent := await self.repo.get_by_id(id)):
            raise HTTPException(status_code=404, detail='Интент не найден')
        return intent

    async def get_by_bot_guid_and_name(self, bot_guid: str, name: str) -> Intents:
        """
        Интенты имеют уникальные name для каждого бота, т.е. unique(name, bot_guid).
        """
        if not (intent := await self.repo.get_by_bot_guid_and_name(bot_guid, name)):
            raise HTTPException(status_code=404, detail='Интент не найден')
        return intent

    async def get_by_bot_guid_and_rank(self, bot_guid: str, intent_rank: int) -> Intents:
        if not (intent := await self.repo.get_by_bot_guid_and_rank(bot_guid, intent_rank)):
            raise HTTPException(status_code=404, detail='Интент не найден')
        return intent

    async def get_by_bot_guid_and_msg(self, bot_guid: str, message: str) -> Intents:
        """
        Использовать, если нужно найти команду.
        """
        if not (intent := await self.repo.get_by_bot_guid_and_msg(bot_guid, message)):
            raise HTTPException(status_code=404, detail='Интент не найден')
        return intent

    async def add(self, request: IntentsRequestDB, user: dict) -> Intents:
        if request.rank != -1:
            request.rank = await self.find_intent_rank(request.bot_guid)

        if await self.repo.get_by_bot_guid_and_name(request.bot_guid, request.name):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Полученные данные конфликтуют с существующим интентом')

        return await self.repo.add(request, user.get('user_guid'))

    async def update(self, intent: Intents, request: IntentsRequestDB) -> Intents:
        same_intent = await self.repo.get_by_bot_guid_and_name(request.bot_guid, request.name)

        if same_intent and intent.id != same_intent.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Полученные данные конфликтуют с существующим интентом')

        return await self.repo.update(intent, request)

    async def delete(self, intent: Intents) -> None:
        await self.repo.delete(intent)

    async def find_intent_rank(self, bot_guid: str) -> int:
        ranks = tuple(n.rank for n in await self.get_all_by_bot_guid(bot_guid) if n.rank > -1)
        for i, r in enumerate(ranks):
            if r != i:
                return i
        return max(ranks, default=-1) + 1

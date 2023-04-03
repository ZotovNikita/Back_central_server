from typing import List
from fastapi import Depends
from src.repositories.admin_chat import AdminChatRepository
from src.models.admin_chat_log import AdminChatLog
from src.models.intents import Intents
from src.models.schemas.admin_chat.request import AdminChatRequest
from src.services.intents import IntentsService
from src.services.bots import BotsService


class AdminChatService:
    def __init__(self, repository: AdminChatRepository = Depends(), intents_service: IntentsService = Depends(), bots_service: BotsService = Depends()):
        self.repo = repository
        self.intents_service = intents_service
        self.bots_service = bots_service

    async def log(self, request: AdminChatRequest, user_info: dict, intent: Intents) -> None:
        await self.bots_service.get_by_guid(request.bot_guid)

        record = AdminChatLog(
            **dict(request),
            user_guid=user_info.get('user_guid'),
            intent_rank=intent.rank,
            answer=intent.answer,
        )

        await self.repo.add(record)

    async def answer(self, request: AdminChatRequest, current_user: dict) -> Intents:
        answer = await self.intents_service.find_intent_by_msg(request.bot_guid, request.message)
        await self.log(request, current_user, answer)
        return answer

    async def get_chat_history(self, bot_guid: str, user: dict) -> List[AdminChatLog]:
        return await self.repo.get_all_by_bot_guid_and_user_guid(bot_guid, user.get('user_guid'))

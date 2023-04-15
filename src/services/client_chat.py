from typing import List
from fastapi import HTTPException, Depends
from src.core.settings import settings
from src.repositories.client_chat import ClientChatRepository
from src.models.client_chat_log import ClientChatLog
from src.models.intents import Intents
from src.models.schemas.client_chat.request import ClientChatRequest
from src.services.intents import IntentsService
from src.services.bots import BotsService


class ClientChatService:
    def __init__(self, repository: ClientChatRepository = Depends(), intents_service: IntentsService = Depends(), bots_service: BotsService = Depends()):
        self.repo = repository
        self.intents_service = intents_service
        self.bots_service = bots_service

    async def log(self, request: ClientChatRequest, intent: Intents) -> None:
        await self.bots_service.get_by_guid(request.bot_guid)

        record = ClientChatLog(
            **dict(request),
            in_doubt=False,
            intent_rank=intent.rank,
            answer=intent.answer,
        )

        await self.repo.add(record)

    async def answer(self, request: ClientChatRequest) -> Intents:
        if request.message == settings.in_doubt_command:
            if (last_message := await self.repo.get_last_by_bot_guid_and_client_id(request.bot_guid, request.client_id)):
                await self.repo.update_doubt_status(last_message, True)
            raise HTTPException(status_code=200, detail='Последнее сообщение клиента успешно отмечено как сомнительное')

        answer = await self.intents_service.find_intent_by_msg(request.bot_guid, request.message)
        await self.log(request, answer)
        return answer

    async def get_bot_history(self, bot_guid: str) -> List[ClientChatLog]:
        return await self.repo.get_all_by_bot_guid(bot_guid)

    async def get_all_in_doubt_by_bot_guid(self, bot_guid: str) -> List[ClientChatLog]:
        return await self.repo.get_all_by_doubt_status_and_bot_guid(True, bot_guid)

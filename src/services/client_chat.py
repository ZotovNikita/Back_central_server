from fastapi import Depends
from src.repositories.client_chat import ClientChatRepository
from src.models.client_chat_log import ClientChatLog
from src.models.intents import Intents
from src.models.schemas.client_chat.client_chat_request import ClientChatRequest
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
        answer = await self.intents_service.find_intent_by_msg(request.bot_guid, request.message)
        await self.log(request, answer)
        return answer

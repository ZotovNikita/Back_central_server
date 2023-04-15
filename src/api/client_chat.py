from typing import List
from pydantic import UUID4
from fastapi import APIRouter, Depends
from src.services.client_chat import ClientChatService
from src.models.schemas.client_chat.request import ClientChatRequest
from src.models.schemas.client_chat.response import ClientChatResponse
from src.models.schemas.intents.response import IntentsResponse
from src.dependencies import ADMIN_ONLY


router = APIRouter(
    prefix='/client_chat',
    tags=['client_chat'],
)


@router.post('/answer', response_model=IntentsResponse, name='Получить ответ от бота')
async def answer(request: ClientChatRequest, service: ClientChatService = Depends()):
    return await service.answer(request)


@router.get('/history/{bot_guid}', response_model=List[ClientChatResponse], name='Получить историю сообщений бота', dependencies=[Depends(ADMIN_ONLY)])
async def get_bot_history(bot_guid: UUID4, service: ClientChatService = Depends()):
    return await service.get_bot_history(bot_guid)


@router.get('/doubt/{bot_guid}', response_model=List[ClientChatResponse], name='Получить все сомнительные сообщения бота', dependencies=[Depends(ADMIN_ONLY)])
async def get_all_in_doubt_by_bot_guid(bot_guid: UUID4, service: ClientChatService = Depends()):
    return await service.get_all_in_doubt_by_bot_guid(bot_guid)

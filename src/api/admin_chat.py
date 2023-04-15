from typing import List
from pydantic import UUID4
from fastapi import APIRouter, Depends
from src.services.admin_chat import AdminChatService
from src.models.schemas.admin_chat.request import AdminChatRequest
from src.models.schemas.admin_chat.response import AdminChatResponse
from src.models.schemas.intents.response import IntentsResponse
from src.dependencies import AUTHORIZED


router = APIRouter(
    prefix='/admin_chat',
    tags=['admin_chat'],
    dependencies=[Depends(AUTHORIZED)],
)


@router.post('/answer', response_model=IntentsResponse, name='Получить ответ от бота')
async def answer(request: AdminChatRequest, service: AdminChatService = Depends(), current_user: dict = Depends(AUTHORIZED)):
    return await service.answer(request, current_user)


@router.get('/history', response_model=List[AdminChatResponse], name='Получить историю чата')
async def get_chat_history(bot_guid: UUID4, service: AdminChatService = Depends(), current_user: dict = Depends(AUTHORIZED)):
    return await service.get_chat_history(bot_guid, current_user)

from fastapi import APIRouter, Depends
from src.services.admin_chat import AdminChatService
from src.models.schemas.admin_chat.admin_chat_request import AdminChatRequest
from src.models.schemas.intents.intents_response import IntentsResponse
from src.dependencies import AUTHORIZED


router = APIRouter(
    prefix='/admin_chat',
    tags=['admin_chat'],
    dependencies=[Depends(AUTHORIZED)],
)


@router.post('/answer', response_model=IntentsResponse, name='Получить ответ от бота')
async def answer(request: AdminChatRequest, service: AdminChatService = Depends(), current_user: dict = Depends(AUTHORIZED)):
    return await service.answer(request, current_user)

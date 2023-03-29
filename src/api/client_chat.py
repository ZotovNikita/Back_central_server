from fastapi import APIRouter, Depends
from src.services.client_chat import ClientChatService
from src.models.schemas.client_chat.client_chat_request import ClientChatRequest
from src.models.schemas.intents.intents_response import IntentsResponse


router = APIRouter(
    prefix='/client_chat',
    tags=['client_chat'],
)


@router.post('/answer', response_model=IntentsResponse, name='Получить ответ от бота')
async def answer(request: ClientChatRequest, service: ClientChatService = Depends()):
    return await service.answer(request)

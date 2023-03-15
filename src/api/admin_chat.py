from fastapi import APIRouter, Depends
from src.services.auth import get_current_user
from src.services.admin_chat import AdminChatService
from src.models.schemas.admin_chat.admin_chat_request import AdminChatRequest
from src.models.schemas.intents.intents_response import IntentsResponse


router = APIRouter(
    prefix='/admin_chat',
    tags=['admin_chat'],
    dependencies=[Depends(get_current_user)],
)


@router.post('/answer', response_model=IntentsResponse, name='Получить ответ от бота')
def answer(request: AdminChatRequest, service: AdminChatService = Depends()):
    return service.answer(request)

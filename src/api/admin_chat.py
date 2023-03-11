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


@router.post('/predict', response_model=IntentsResponse, name='Предсказание интента от модели')
def predict(request: AdminChatRequest, service: AdminChatService = Depends()):
    return service.predict_intent(request)

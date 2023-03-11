from fastapi import APIRouter, Depends
from src.services.client_chat import ClientChatService
from src.models.schemas.client_chat.client_chat_request import ClientChatRequest
from src.models.schemas.intents.intents_response import IntentsResponse


router = APIRouter(
    prefix='/client_chat',
    tags=['client_chat'],
)


@router.post('/predict', response_model=IntentsResponse, name='Предсказание интента от модели')
def predict(request: ClientChatRequest, service: ClientChatService = Depends()):
    return service.predict_intent(request)

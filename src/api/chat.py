from fastapi import APIRouter, Depends
from src.services.auth import get_current_user
from src.services.chat import ChatService
from src.models.schemas.chat.chat_request import ChatRequest
from src.models.schemas.intents.intents_response import IntentsResponse


router = APIRouter(
    prefix='/chat',
    tags=['chat'],
    dependencies=[Depends(get_current_user)],
)


# ! post/get ?
@router.post('/predict', response_model=IntentsResponse, name='Предсказание интента от модели')
def predict(request: ChatRequest, service: ChatService = Depends()):
    return service.predict_intent(request)

from fastapi import APIRouter, Depends
from pydantic import UUID4
from src.services.auth import get_current_user
from src.models.schemas.bot_data.bot_data_request import BotDataRequest
from src.models.schemas.bot_data.bot_data_response import BotDataResponse


router = APIRouter(
    prefix='/bots',
    tags=['bots'],
    dependencies=[Depends(get_current_user)],
)


@router.get('/intents', name='Тест получения интентов')
def get(bot_guid: UUID4):
    print(bot_guid)
    data = {f'Intent {i}': f'Что-то {i}' for i in range(30)}
    return data


@router.post('/predict', response_model=BotDataResponse, name='Тест запроса от ботов')
def predict(request: BotDataRequest):
    msg = 'Done_' + request.message
    return {'message': msg}

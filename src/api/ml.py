from pydantic import UUID4
from fastapi import APIRouter, Depends
from src.services.ml import MLService
from src.services.intents import IntentsService
from src.services.admin_chat import AdminChatService
from src.dependencies import AUTHORIZED


router = APIRouter(
    prefix='/ml',
    tags=['ml'],
    dependencies=[Depends(AUTHORIZED)],
)


@router.post('/train/{bot_guid}', name='Обучить модель по guid бота')
async def train_bot_model(bot_guid: UUID4, service: MLService = Depends(), intents_service: IntentsService = Depends()):
    intents = await intents_service.get_all_by_bot_guid(bot_guid)
    examples = []
    ranks = []
    for intent in intents:
        if intent.rank < 0:
            continue
        examples += list(map(lambda x: x.text, intent.examples))
        ranks += [intent.rank] * len(intent.examples)
    return await service.train(bot_guid, examples, ranks)


@router.post('/step/{bot_guid}/{intent_name:path}', name='Шаг обучения модели бота')
async def step(bot_guid: UUID4, intent_name: str, service: MLService = Depends(), intents_service: IntentsService = Depends(), chat_service: AdminChatService = Depends(), user: dict = Depends(AUTHORIZED)):
    intent = await intents_service.get_by_bot_guid_and_name(bot_guid, intent_name)
    message = await chat_service.get_last_user_message(bot_guid, user)
    return await service.step(bot_guid, message.message, intent.rank)

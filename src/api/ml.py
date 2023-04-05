from pydantic import UUID4
from fastapi import APIRouter, Depends
from src.services.ml import MLService
from src.services.intents import IntentsService
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

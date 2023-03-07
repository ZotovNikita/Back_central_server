from typing import List
from fastapi import APIRouter, Depends
from pydantic import UUID4
from src.services.auth import get_current_user
from src.services.intents import IntentsService
from src.models.schemas.intents.intents_response import IntentsResponse


router = APIRouter(
    prefix='/intents',
    tags=['intents'],
    dependencies=[Depends(get_current_user)],
)


@router.get('/{bot_guid}', response_model=List[IntentsResponse], name='Получить все интенты бота')
def get(bot_guid: UUID4, service: IntentsService = Depends()):
    return service.all_intents_for_bot(bot_guid)

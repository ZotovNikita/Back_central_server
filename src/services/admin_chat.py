from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.intents import Intents
from src.models.schemas.admin_chat.admin_chat_request import AdminChatRequest
from src.services.ml import MLService
from src.services.intents import IntentsService


class AdminChatService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
    
    def predict_intent(self, request: AdminChatRequest) -> Intents:
        intent_rank = MLService.predict(request.bot_guid, request.message)
        intent = IntentsService(self.session).get_by_guid_and_rank(request.bot_guid, intent_rank)
        return intent

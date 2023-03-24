from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.admin_chat_log import AdminChatLog
from src.models.intents import Intents
from src.models.schemas.admin_chat.admin_chat_request import AdminChatRequest
from src.services.ml import MLService
from src.services.intents import IntentsService
from src.services.bots import BotsService
from functions import is_command


class AdminChatService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
    
    def log(self, request: AdminChatRequest, user_info: dict, intent: Intents = None) -> None:
        BotsService(self.session).get(request.bot_guid)
        
        rec = AdminChatLog(
            message=request.message,
            user_guid=user_info.get('user_guid'),
            bot_guid=request.bot_guid,
            intent_rank=None if intent is None else intent.rank
        )
        
        self.session.add(rec)
        self.session.commit()
    
    def predict_intent(self, request: AdminChatRequest) -> Intents:
        intent_rank = MLService.predict(request.bot_guid, request.message)
        intent = IntentsService(self.session).get_by_guid_and_rank(request.bot_guid, intent_rank)
        return intent

    def answer(self, request: AdminChatRequest, current_user: dict) -> Intents:
        self.log(request, current_user)
        
        answer: Intents
        if is_command(request.message):
            answer = IntentsService(self.session).get_by_guid_and_msg(request.bot_guid, request.message)
        else:
            answer = self.predict_intent(request)
        
        self.log(request, current_user, answer)
        return answer

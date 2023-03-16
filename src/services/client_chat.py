from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.intents import Intents
from src.models.client_chat_log import ClientChatLog
from src.models.schemas.client_chat.client_chat_request import ClientChatRequest
from src.services.ml import MLService
from src.services.intents import IntentsService
from src.services.bots import BotsService
from src.services.utils.checkers import is_command


class ClientChatService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
    
    def log(self, request: ClientChatRequest, intent: Intents = None) -> None:
        BotsService(self.session).get(request.bot_guid)
        
        rec = ClientChatLog(
            message=request.message,
            in_doubt=False,
            client_id=request.client_id,
            bot_guid=request.bot_guid,
            intent_rank=None if intent is None else intent.rank
        )
        
        self.session.add(rec)
        self.session.commit()
    
    def predict_intent(self, request: ClientChatRequest) -> Intents:
        intent_rank = MLService.predict(request.bot_guid, request.message)
        intent = IntentsService(self.session).get_by_guid_and_rank(request.bot_guid, intent_rank)
        return intent

    def answer(self, request: ClientChatRequest) -> Intents:
        self.log(request)
        
        answer: Intents
        if is_command(request.message):
            answer = IntentsService(self.session).get_by_guid_and_msg(request.bot_guid, request.message)
        else:
            answer = self.predict_intent(request)
        
        self.log(request, answer)
        return answer

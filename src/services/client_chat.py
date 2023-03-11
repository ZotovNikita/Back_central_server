from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.intents import Intents
from src.models.schemas.client_chat.client_chat_request import ClientChatRequest
from src.services.ml import MLService


class ClientChatService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
    
    def predict_intent(self, request: ClientChatRequest) -> Intents:
        intent_rank = MLService.predict(request.bot_guid, request.message)
        
        intent = (
            self.session
            .query(Intents)
            .filter(Intents.bot_guid == request.bot_guid, Intents.rank == intent_rank)
            .one_or_none()
        )
        
        if not intent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Интент не найден')
        
        return intent

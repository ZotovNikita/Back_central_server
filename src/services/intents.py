from typing import List
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.intents import Intents


class IntentsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
    
    def get_by_guid_and_rank(self, bot_guid: str, intent_rank: int) -> Intents:
        intent = (
            self.session
            .query(Intents)
            .filter(Intents.bot_guid == bot_guid, Intents.rank == intent_rank)
            .one_or_none()
        )
        
        if not intent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Интент не найден')
        
        return intent
    
    def all_intents_for_bot(self, bot_guid: str) -> List[Intents]:
        intents = (
            self.session
            .query(Intents)
            .filter(Intents.bot_guid == bot_guid)
            .order_by(Intents.rank.asc())
            .all()
        )
        
        return intents

from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.intents import Intents


class IntentsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
    
    def all_intents_for_bot(self, bot_guid: str) -> List[Intents]:
        intents = (
            self.session
            .query(Intents)
            .filter(Intents.bot_guid == bot_guid)
            .order_by(Intents.rank.asc())
            .all()
        )
        
        return intents

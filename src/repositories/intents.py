from typing import Optional, List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.intents import Intents
from src.models.schemas.intents.intents_request import IntentsRequestDB


class IntentsRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def get_all(self) -> List[Intents]:
        intents = (
            self.session
            .query(Intents)
            .all()
        )
        return intents

    async def get_all_by_bot_guid(self, bot_guid: str) -> List[Intents]:
        intents = (
            self.session
            .query(Intents)
            .filter_by(bot_guid=bot_guid)
            .order_by(Intents.rank.asc())
            .all()
        )
        return intents

    async def get_by_id(self, id: int) -> Optional[Intents]:
        intent = (
            self.session
            .query(Intents)
            .filter_by(id=id)
            .first()
        )
        return intent

    async def get_by_bot_guid_and_name(self, bot_guid: str, name: str) -> Optional[Intents]:
        """
        Интенты имеют уникальные name для каждого бота, т.е. unique(name, bot_guid).
        """
        intent = (
            self.session
            .query(Intents)
            .filter_by(bot_guid=bot_guid, name=name)
            .first()
        )
        return intent

    async def get_by_bot_guid_and_rank(self, bot_guid: str, intent_rank: int) -> Optional[Intents]:
        intent = (
            self.session
            .query(Intents)
            .filter_by(bot_guid=bot_guid, rank=intent_rank)
            .first()
        )
        return intent

    async def get_by_bot_guid_and_msg(self, bot_guid: str, message: str) -> Optional[Intents]:
        """
        Использовать, если нужно найти команду.
        """
        intent = (
            self.session
            .query(Intents)
            .filter_by(bot_guid=bot_guid, name=message)
            .first()
        )
        return intent

    async def add(self, request: IntentsRequestDB, user_guid: str) -> Intents:
        intent = Intents(
            name=request.name,
            answer=request.answer,
            rank=request.rank,
            bot_guid=request.bot_guid,
            created_by=user_guid,
        )
        self.session.add(intent)
        self.session.commit()
        return intent

    async def update(self, intent: Intents, request: IntentsRequestDB) -> Intents:
        for field, value in request:
            setattr(intent, field, value)
        self.session.commit()
        return intent

    async def delete(self, intent: Intents) -> None:
        self.session.delete(intent)
        self.session.commit()

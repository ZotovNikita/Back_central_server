from typing import List, Optional
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.services.users import create_by
from src.models.intents import Intents
from src.models.schemas.intents.intents_request import IntentsRequestDB


class IntentsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def get(self, id: int) -> Intents:
        intent = (
            self.session
            .query(Intents)
            .filter(Intents.id == id)
            .one_or_none()
        )

        if not intent:
            raise HTTPException(status_code=404, detail='Интент не найден')

        return intent

    async def all(self) -> List[Intents]:
        intents = (
            self.session
            .query(Intents)
            .all()
        )

        if not intents:
            raise HTTPException(status_code=404)

        return intents

    async def add(self, request: IntentsRequestDB, user: dict) -> Intents:
        if request.rank != -1:
            request.rank = await self.find_intent_rank(request.bot_guid)

        is_exist = (
            self.session
            .query(Intents)
            .filter_by(bot_guid=request.bot_guid, name=request.name)
            .count()
        )
        if is_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        intent = await create_by(Intents(), request, user)

        self.session.add(intent)
        self.session.commit()
        return intent

    async def update(self, id: int, request: IntentsRequestDB) -> Intents:
        intent = await self.get(id)
        same_intent = await self.get_by_bot_guid_and_name(request.bot_guid, request.name)

        if same_intent and id != same_intent.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        for field, value in request:
            setattr(intent, field, value)

        self.session.commit()
        return intent

    async def delete(self, id: int) -> None:
        intent = await self.get(id)
        self.session.delete(intent)
        self.session.commit()

    async def all_intents_for_bot(self, bot_guid: str) -> List[Intents]:
        intents = (
            self.session
            .query(Intents)
            .filter(Intents.bot_guid == bot_guid)
            .order_by(Intents.rank.asc())
            .all()
        )

        return intents

    async def get_by_bot_guid_and_name(self, bot_guid: str, name: str) -> Optional[Intents]:
        """
        Интенты имеют уникальные name для каждого бота, т.е. unique(name, bot_guid).
        """
        intent = (
            self.session
            .query(Intents)
            .filter_by(bot_guid=bot_guid, name=name)
            .one_or_none()
        )

        return intent

    async def get_by_guid_and_rank(self, bot_guid: str, intent_rank: int) -> Intents:
        intent = (
            self.session
            .query(Intents)
            .filter(Intents.bot_guid == bot_guid, Intents.rank == intent_rank)
            .one_or_none()
        )

        if not intent:
            raise HTTPException(status_code=404, detail='Интент не найден')

        return intent

    async def get_by_guid_and_msg(self, bot_guid: str, message: str) -> Intents:
        intent = (
            self.session
            .query(Intents)
            .filter(Intents.bot_guid == bot_guid, Intents.name == message)
            .one_or_none()
        )

        if not intent:
            raise HTTPException(status_code=404, detail='Интент не найден')

        return intent

    async def update_by_bot_guid_and_name(self, bot_guid: str, name: str, request: IntentsRequestDB) -> Intents:
        intent = await self.get_by_bot_guid_and_name(bot_guid, name)

        if not intent:
            raise HTTPException(status_code=404, detail='Интент не найден')

        same_intent = await self.get_by_bot_guid_and_name(request.bot_guid, request.name)

        if same_intent and intent.id != same_intent.id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        for field, value in request:
            setattr(intent, field, value)

        self.session.commit()
        return intent

    async def delete_by_bot_guid_and_name(self, bot_guid: str, name: str) -> None:
        intent = await self.get_by_bot_guid_and_name(bot_guid, name)

        if not intent:
            raise HTTPException(status_code=404, detail='Интент не найден')

        self.session.delete(intent)
        self.session.commit()

    async def find_intent_rank(self, bot_guid: str) -> int:
        ranks = tuple(n.rank for n in await self.all_intents_for_bot(bot_guid) if n.rank > -1)
        for i, r in enumerate(ranks):
            if r != i:
                return i
        return max(ranks) + 1

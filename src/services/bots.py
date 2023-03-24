from typing import List
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.bots import Bots
from src.models.relations import Relations
from src.models.schemas.bots.bots_request import BotsRequest


class BotsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Bots]:
        bots = (
            self.session
            .query(Bots)
            .all()
        )

        if not bots:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return bots

    def get(self, guid: str) -> Bots:
        bot = (
            self.session
            .query(Bots)
            .filter(Bots.guid == guid)
            .one_or_none()
        )

        if not bot:
            raise HTTPException(status_code=404, detail='Бот не найден')

        return bot

    def add(self, request: BotsRequest) -> Bots:
        is_exist = (
            self.session
            .query(Bots)
            .filter(Bots.guid == request.guid)
            .count()
        )
        if is_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        bot = Bots()
        for field, value in request:
            setattr(bot, field, value)

        self.session.add(bot)
        self.session.commit()
        return bot

    def update(self, guid: str, request: BotsRequest) -> Bots:
        bot = self.get(guid)

        with_same_guid = self.get(request.guid)
        if with_same_guid and guid != with_same_guid.guid:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        for field, value in request:
            setattr(bot, field, value)

        self.session.commit()
        return bot

    def delete(self, guid: str) -> None:
        bot = self.get(guid)
        self.session.delete(bot)
        self.session.commit()

    def allowed_bots_for_user(self, current_user: dict) -> List[Bots]:
        bots = (
            self.session
            .query(Bots.name, Bots.guid)
            .join(Relations, Relations.bot_guid == Bots.guid)
            .filter(Relations.user_guid == current_user.get('user_guid'))
            .order_by(Bots.name.asc())
            .all()
        )

        return bots

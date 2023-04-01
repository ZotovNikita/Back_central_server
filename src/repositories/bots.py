from typing import Optional, List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.repositories.users import UsersRepository
from src.models.bots import Bots
from src.models.schemas.bots.request import BotsRequest


class BotsRepository:
    def __init__(self, session: Session = Depends(get_session), users_repository: UsersRepository = Depends()):
        self.session = session
        self.users_repo = users_repository

    async def get_all(self) -> List[Bots]:
        bots = (
            self.session
            .query(Bots)
            .all()
        )
        return bots

    async def get_all_by_user_guid(self, user_guid: str) -> List[Bots]:
        """
        SELECT Bots.name, Bots.guid
        FROM Bots
        JOIN Relations
        ON Relations.bot_guid = Bots.guid
        WHERE Relations.user_guid = user_guid
        ORDER BY Bots.name ASC
        """
        # bots = (
        #     self.session
        #     .query(Bots)
        #     .join(Relations, Relations.bot_guid == Bots.guid)
        #     .filter(Relations.user_guid == user_guid)
        #     .order_by(Bots.name.asc())
        #     .all()
        # )
        user = await self.users_repo.get_by_guid(user_guid)
        return user.bots

    async def get_by_guid(self, guid: str) -> Optional[Bots]:
        bot = (
            self.session
            .query(Bots)
            .filter_by(guid=guid)
            .first()
        )
        return bot

    async def add(self, request: BotsRequest) -> Bots:
        bot = Bots(**dict(request))
        self.session.add(bot)
        self.session.commit()
        return bot

    async def update(self, bot: Bots, request: BotsRequest) -> Bots:
        for field, value in request:
            setattr(bot, field, value)
        self.session.commit()
        return bot

    async def delete(self, bot: Bots) -> None:
        self.session.delete(bot)
        self.session.commit()
from typing import Optional, List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.relations import Relations
from src.models.schemas.relations.request import RelationsRequestDB


class RelationsRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def get_all(self) -> List[Relations]:
        relations = (
            self.session
            .query(Relations)
            .all()
        )
        return relations

    async def get_by_id(self, id: int) -> Optional[Relations]:
        relation = (
            self.session
            .query(Relations)
            .filter_by(id=id)
            .first()
        )
        return relation

    async def get_by_user_guid_and_bot_guid(self, user_guid: str, bot_guid: str) -> Optional[Relations]:
        relation = (
            self.session
            .query(Relations)
            .filter_by(user_guid=user_guid, bot_guid=bot_guid)
            .first()
        )
        return relation

    async def add(self, request: RelationsRequestDB) -> Relations:
        relation = Relations(**dict(request))
        self.session.add(relation)
        self.session.commit()
        return relation

    async def update(self, relation: Relations, request: RelationsRequestDB) -> Relations:
        for field, value in request:
            setattr(relation, field, value)
        self.session.commit()
        return relation

    async def delete(self, relation: Relations) -> None:
        self.session.delete(relation)
        self.session.commit()

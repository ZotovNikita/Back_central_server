from typing import Optional, List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.users import Users
from src.models.schemas.users.request import UsersRequestDB


class UsersRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def get_all(self) -> List[Users]:
        users = (
            self.session
            .query(Users)
            .all()
        )
        return users

    async def get_by_guid(self, guid: str) -> Optional[Users]:
        user = (
            self.session
            .query(Users)
            .filter_by(guid=guid)
            .first()
        )
        return user

    async def get_by_login(self, login: str) -> Optional[Users]:
        user = (
            self.session
            .query(Users)
            .filter_by(login=login)
            .first()
        )
        return user

    async def add(self, request: UsersRequestDB) -> Users:
        user = Users(**dict(request))
        self.session.add(user)
        self.session.commit()
        return user

    async def update(self, user: Users, request: UsersRequestDB) -> Users:
        for field, value in request:
            setattr(user, field, value)
        self.session.commit()
        return user

    async def delete(self, user: Users) -> None:
        self.session.delete(user)
        self.session.commit()

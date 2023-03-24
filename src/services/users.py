from typing import List
from pydantic import BaseModel
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.base import Base
from src.models.users import Users
from src.models.schemas.users.users_request import UsersRequest
from src.services.secure import SecureService


def create_by(model: Base, schema: BaseModel, user: dict) -> Base:
    for field, value in schema:
        setattr(model, field, value)
    setattr(model, 'created_by', user.get('user_guid'))
    return model


class UsersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def all(self) -> List[Users]:
        users = (
            self.session
            .query(Users)
            .all()
        )

        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return users

    def get(self, guid: str) -> Users:
        user = (
            self.session
            .query(Users)
            .filter(Users.guid == guid)
            .one_or_none()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')

        return user

    def add(self, request: UsersRequest) -> Users:
        is_exist = (
            self.session
            .query(Users)
            .filter(Users.login == request.login)
            .count()
        )
        if is_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        user = Users(
            login=request.login,
            password_hashed=SecureService.hash_password(request.password_text)
        )

        self.session.add(user)
        self.session.commit()
        return user

    def update(self, guid: str, request: UsersRequest) -> Users:
        user = self.get(guid)

        with_same_login = (
            self.session
            .query(Users)
            .filter(Users.login == request.login)
            .first()
        )
        if with_same_login and guid != with_same_login.guid:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        setattr(user, 'login', request.login)
        setattr(user, 'password_hashed', SecureService.hash_password(request.password_text))

        self.session.commit()
        return user

    def delete(self, guid: str) -> None:
        user = self.get(guid)
        self.session.delete(user)
        self.session.commit()

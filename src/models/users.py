from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from src.models.base import Base


class Users(Base):
    __tablename__ = 'users'
    guid = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    login = Column(String, nullable=False, unique=True)
    password_hashed = Column(String, nullable=False)
    relations = relationship('Relations', back_populates='user', cascade='all, delete-orphan')
    bots = relationship('Bots', secondary='relations', viewonly=True, lazy='subquery')

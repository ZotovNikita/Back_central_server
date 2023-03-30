from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from src.models.base import Base


class Bots(Base):
    __tablename__ = 'bots'
    guid = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE)
    name = Column(String, nullable=False)
    relations = relationship('Relations', back_populates='bot', cascade='all, delete-orphan')
    users = relationship('Users', secondary='relations', viewonly=True, lazy='subquery')
    intents = relationship('Intents', backref='bot', cascade='all, delete-orphan')

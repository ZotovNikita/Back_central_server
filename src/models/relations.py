from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from fastapi_utils.guid_type import GUID
from src.models.base import Base


class Relations(Base):
    __tablename__ = 'relations'
    metadata = Base.metadata
    user_guid = Column(GUID, ForeignKey('users.guid'), primary_key=True)
    bot_guid = Column(GUID, ForeignKey('bots.guid'), primary_key=True)
    user = relationship('Users', back_populates='relations')
    bot = relationship('Bots', back_populates='relations')

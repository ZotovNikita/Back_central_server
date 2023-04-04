from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from fastapi_utils.guid_type import GUID
from src.models.base import Base


class Relations(Base):
    __tablename__ = 'relations'
    metadata = Base.metadata
    user_guid = Column(GUID, ForeignKey('users.guid', name='fk_relations__user_guid', ondelete='CASCADE'), primary_key=True)
    bot_guid = Column(GUID, ForeignKey('bots.guid', name='fk_relations__bot_guid', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    user = relationship('Users', back_populates='relations')
    bot = relationship('Bots', back_populates='relations')

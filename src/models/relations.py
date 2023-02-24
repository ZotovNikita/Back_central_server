from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from fastapi_utils.guid_type import GUID
from src.models.base import Base
from src.models import users, bots


class Relations(Base):
    __tablename__ = 'relations'
    id = Column(Integer, primary_key=True)
    user_guid = Column(GUID, ForeignKey('users.guid'), nullable=False)
    bot_guid = Column(GUID, ForeignKey('bots.guid'), nullable=False)
    user = relationship('Users', backref='relations_user')
    bot = relationship('Bots', backref='relations_bot')

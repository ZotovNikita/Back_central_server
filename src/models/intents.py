from sqlalchemy import Column, ForeignKey, Integer, String
from fastapi_utils.guid_type import GUID
from src.models.base import Base


class Intents(Base):
    __tablename__ = 'intents'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    rank = Column(Integer, nullable=True)
    bot_guid = Column(GUID, ForeignKey('bots.guid'), nullable=False)
    created_by = Column(GUID, ForeignKey('users.guid'), nullable=False)

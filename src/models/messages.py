from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID
from src.models.base import Base


class Messages(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    intent_id = Column(Integer, ForeignKey('intents.id'), nullable=True)
    user_guid = Column(GUID, ForeignKey('users.guid'), nullable=False)
    bot_guid = Column(GUID, ForeignKey('bots.guid'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID
from src.models.base import Base


class AdminChatLog(Base):
    __tablename__ = 'admin_chat_log'
    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    user_guid = Column(GUID, ForeignKey('users.guid', ondelete='CASCADE'), nullable=False)
    bot_guid = Column(GUID, ForeignKey('bots.guid', ondelete='CASCADE'), nullable=False)
    intent_rank = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

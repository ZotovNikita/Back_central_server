from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID
from src.models.base import Base


class ClientChatLog(Base):
    __tablename__ = 'client_chat_log'
    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    in_doubt = Column(Boolean, nullable=True)
    client_id = Column(String, nullable=False)
    bot_guid = Column(GUID, ForeignKey('bots.guid', name='fk_client_chat_log__bot_guid', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    intent_rank = Column(Integer, nullable=False)
    answer = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

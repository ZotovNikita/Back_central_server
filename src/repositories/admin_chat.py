from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.admin_chat_log import AdminChatLog


class AdminChatRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def get_all_by_bot_guid_and_user_guid(self, bot_guid: str, user_guid: str) -> List[AdminChatLog]:
        answers = (
            self.session
            .query(AdminChatLog)
            .filter_by(bot_guid=bot_guid, user_guid=user_guid)
            .order_by(AdminChatLog.created_at.asc())
            .all()
        )
        return answers

    async def add(self, record: AdminChatLog) -> None:
        self.session.add(record)
        self.session.commit()

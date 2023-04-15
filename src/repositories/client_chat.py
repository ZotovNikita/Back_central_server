from typing import Optional, List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.db.db import get_session
from src.models.client_chat_log import ClientChatLog


class ClientChatRepository:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    async def add(self, record: ClientChatLog) -> None:
        self.session.add(record)
        self.session.commit()

    async def get_last_by_bot_guid_and_client_id(self, bot_guid: str, client_id: str) -> Optional[ClientChatLog]:
        record = (
            self.session
            .query(ClientChatLog)
            .filter_by(bot_guid=bot_guid, client_id=client_id)
            .order_by(ClientChatLog.created_at.desc())
            .first()
        )
        return record

    async def get_all_by_bot_guid(self, bot_guid: str) -> List[ClientChatLog]:
        records = (
            self.session
            .query(ClientChatLog)
            .filter_by(bot_guid=bot_guid)
            .order_by(ClientChatLog.created_at.asc())
            .all()
        )
        return records

    async def get_all_by_doubt_status_and_bot_guid(self, in_doubt: bool, bot_guid: str) -> List[ClientChatLog]:
        records = (
            self.session
            .query(ClientChatLog)
            .filter_by(in_doubt=in_doubt, bot_guid=bot_guid)
            .order_by(ClientChatLog.created_at.asc())
            .all()
        )
        return records

    async def update_doubt_status(self, record: ClientChatLog, in_doubt: bool) -> ClientChatLog:
        setattr(record, 'in_doubt', in_doubt)
        self.session.commit()
        return record

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

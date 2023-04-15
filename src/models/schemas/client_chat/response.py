from pydantic import BaseModel, UUID4
from datetime import datetime


class ClientChatResponse(BaseModel):
    id: int
    message: str
    in_doubt: bool
    client_id: str
    bot_guid: UUID4
    intent_rank: int
    answer: str
    created_at: datetime

    class Config:
        orm_mode = True

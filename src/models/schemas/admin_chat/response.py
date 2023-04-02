from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


class AdminChatResponse(BaseModel):
    id: int
    message: str
    user_guid: UUID4
    bot_guid: UUID4
    intent_rank: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True

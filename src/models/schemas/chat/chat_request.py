from pydantic import BaseModel, UUID4


class ChatRequest(BaseModel):
    bot_guid: UUID4
    message: str

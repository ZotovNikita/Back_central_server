from pydantic import BaseModel, UUID4


class AdminChatRequest(BaseModel):
    bot_guid: UUID4
    message: str

from pydantic import BaseModel, UUID4


class ClientChatRequest(BaseModel):
    bot_guid: UUID4
    message: str
    client_id: str

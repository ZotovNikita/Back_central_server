from pydantic import BaseModel, UUID4


class BotDataRequest(BaseModel):
    guid: UUID4
    message: str

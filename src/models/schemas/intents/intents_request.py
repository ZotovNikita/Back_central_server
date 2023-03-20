from pydantic import BaseModel, UUID4


class IntentsRequest(BaseModel):
    name: str
    answer: str
    bot_guid: UUID4


class IntentsRequestAdmin(BaseModel):
    name: str
    answer: str
    rank: int
    bot_guid: UUID4

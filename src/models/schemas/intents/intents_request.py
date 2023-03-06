from pydantic import BaseModel, UUID4


class IntentsRequest(BaseModel):
    name: str
    answer: str
    bot_guid: UUID4

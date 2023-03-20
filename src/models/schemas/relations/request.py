from pydantic import BaseModel, UUID4


class RelationsRequest(BaseModel):
    id: int
    user_guid: UUID4
    bot_guid: UUID4

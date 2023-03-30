from pydantic import BaseModel, UUID4


class RelationsRequestDB(BaseModel):
    user_guid: UUID4
    bot_guid: UUID4

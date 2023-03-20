from pydantic import BaseModel, UUID4
from src.models.schemas.users.users_response import UsersResponse
from src.models.schemas.bots.bots_response import BotsResponse


class RelationsResponse(BaseModel):
    id: int
    user_guid: UUID4
    bot_guid: UUID4
    user: UsersResponse
    bot: BotsResponse

    class Config:
        orm_mode = True

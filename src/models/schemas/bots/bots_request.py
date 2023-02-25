from pydantic import BaseModel, UUID4


class BotsRequest(BaseModel):
    guid: UUID4
    name: str
    model_name: str

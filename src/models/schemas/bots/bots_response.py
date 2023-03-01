from pydantic import BaseModel, UUID4


class BotsResponse(BaseModel):
    guid: UUID4
    name: str
    model_name: str

    class Config:
        orm_mode = True


class BotsAllowedResponse(BaseModel):
    guid: UUID4
    name: str

    class Config:
        orm_mode = True

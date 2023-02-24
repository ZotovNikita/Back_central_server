from pydantic import BaseModel


class BotDataResponse(BaseModel):
    message: str

    class Config:
        orm_mode = True

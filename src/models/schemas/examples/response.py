from pydantic import BaseModel


class ExamplesResponse(BaseModel):
    id: int
    text: str
    intent_id: int

    class Config:
        orm_mode = True

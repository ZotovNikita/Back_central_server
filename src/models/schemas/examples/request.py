from pydantic import BaseModel


class ExamplesRequest(BaseModel):
    text: str
    intent_id: int

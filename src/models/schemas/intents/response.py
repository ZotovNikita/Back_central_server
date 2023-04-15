from pydantic import BaseModel, UUID4
from typing import Optional, List
from src.models.schemas.examples.response import ExamplesResponse


class IntentsResponse(BaseModel):
    id: int
    name: str
    answer: str
    rank: Optional[int]
    bot_guid: UUID4
    created_by: Optional[UUID4]
    examples: List[ExamplesResponse]

    class Config:
        orm_mode = True

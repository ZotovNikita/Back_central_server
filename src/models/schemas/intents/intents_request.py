from typing import List, Optional
from pydantic import BaseModel, UUID4


class IntentsRequestForm(BaseModel):
    name: str
    answer: str
    rank: Optional[int]
    bot_guid: UUID4
    examples: List[str]


class IntentsRequestDB(BaseModel):
    name: str
    answer: str
    rank: Optional[int]
    bot_guid: UUID4

from typing import List
from pydantic import BaseModel, UUID4


class IntentsRequest(BaseModel):
    name: str
    answer: str
    rank: int
    bot_guid: UUID4
    examples: List[str]

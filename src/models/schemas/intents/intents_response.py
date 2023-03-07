from pydantic import BaseModel, UUID4
from typing import Optional


class IntentsResponse(BaseModel):
    id: int
    name: str
    answer: str
    rank: Optional[int]
    bot_guid: UUID4
    created_by: UUID4
    
    class Config:
        orm_mode = True

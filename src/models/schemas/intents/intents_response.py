from pydantic import BaseModel, UUID4


class IntentsResponse(BaseModel):
    id = int
    name = str
    message = str
    rank = int
    bot_guid = UUID4
    created_by = UUID4
    
    class Config:
        orm_mode = True

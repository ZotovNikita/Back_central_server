from pydantic import BaseModel, UUID4


class UsersResponse(BaseModel):
    guid: UUID4
    login: str

    class Config:
        orm_mode = True

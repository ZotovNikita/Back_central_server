from pydantic import BaseModel


class UsersRequest(BaseModel):
    login: str
    password_text: str


class UsersRequestDB(BaseModel):
    login: str
    password_hashed: str

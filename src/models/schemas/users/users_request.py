from pydantic import BaseModel


class UsersRequest(BaseModel):
    login: str
    password_text: str

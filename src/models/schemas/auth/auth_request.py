from pydantic import BaseModel


class AuthRequest(BaseModel):
    login: str
    password_text: str

from pydantic import BaseModel


class AuthorizationRequest(BaseModel):
    guid: str

from pydantic import BaseModel


class Token(BaseModel):
    access: str
    refresh: str


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"

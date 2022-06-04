from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class UserSignup(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

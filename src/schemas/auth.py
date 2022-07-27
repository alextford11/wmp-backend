from pydantic import BaseModel, EmailStr

from src.schemas.utils import PasswordStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


class UserSignup(BaseModel):
    email: EmailStr
    password: PasswordStr
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

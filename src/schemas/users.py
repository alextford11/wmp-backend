from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: Optional[EmailStr]


class UserPasswordHash(UserBase):
    password_hash: str


class UpdateUserProfile(UserBase):
    first_name: Optional[str]
    last_name: Optional[str]


class GetUserProfile(UpdateUserProfile):
    id: Optional[int]

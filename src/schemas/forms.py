from typing import Union

from pydantic import BaseModel


class SelectInputOptionSchema(BaseModel):
    value: Union[str, int]
    label: str

    class Config:
        orm_mode = True


class SelectInputListSchema(BaseModel):
    options: list[SelectInputOptionSchema]


class SelectGroupInputOptionSchema(BaseModel):
    label: str
    options: list[SelectInputOptionSchema]

    class Config:
        orm_mode = True


class SelectGroupInputListSchema(BaseModel):
    options: list[SelectGroupInputOptionSchema]

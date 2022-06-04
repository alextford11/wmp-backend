from pydantic import BaseModel


class MuscleSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

from typing import Optional

from pydantic import BaseModel

from src.schemas.workouts import BoardWorkoutSchema


class BoardGetSchema(BaseModel):
    id: int
    board_workouts: list[BoardWorkoutSchema] = []
    board_workout_order: list[int] = []
    board_muscle_counts: dict = {}

    class Config:
        orm_mode = True


class CreateBoardSchema(BaseModel):
    user_access_token: Optional[str]

    class Config:
        orm_mode = True


class BoardListSchema(BaseModel):
    boards: list[BoardGetSchema] = []

    class Config:
        orm_mode = True

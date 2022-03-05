from operator import itemgetter

from pydantic import BaseModel


class MuscleSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class WorkoutSchema(BaseModel):
    id: int
    name: str
    related_muscles: list[MuscleSchema] = []

    class Config:
        orm_mode = True


class BoardWorkoutSchema(BaseModel):
    id: int
    sort_value: int
    workout: WorkoutSchema

    class Config:
        orm_mode = True


class BoardGetSchema(BaseModel):
    id: int
    board_workouts: list[BoardWorkoutSchema] = []
    board_workout_order: list[int] = []

    class Config:
        orm_mode = True

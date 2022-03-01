from pydantic import BaseModel


class Muscle(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Workout(BaseModel):
    id: int
    title: str
    muscles: list[Muscle] = []

    class Config:
        orm_mode = True


class BoardWorkout(BaseModel):
    id: int
    sort_value: int
    workout: Workout


class Board(BaseModel):
    board_workouts: list[BoardWorkout] = []

    class Config:
        orm_mode = True

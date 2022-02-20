from pydantic import BaseModel


class Muscle(BaseModel):
    id: str
    name: str


class Muscles(BaseModel):
    __root__ = dict[str, Muscle]


class Workout(BaseModel):
    id: str
    title: str
    muscles: Muscles


class Workouts(BaseModel):
    __root__ = dict[str, Workout]


class Board(BaseModel):
    workouts: Workouts
    workout_order: list[str]

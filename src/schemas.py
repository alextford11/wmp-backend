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
    board_muscle_counts: dict = {}

    class Config:
        orm_mode = True


class UpdateWorkoutOrderSchema(BaseModel):
    workout_order: list


class AddWorkoutSchema(BaseModel):
    workout_id: int


class RemoveWorkoutSchema(BaseModel):
    board_workout_id: int


class WorkoutListSchema(BaseModel):
    workouts: list[WorkoutSchema]

    class Config:
        orm_mode = True

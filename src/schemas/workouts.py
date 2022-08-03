from typing import Optional

from pydantic import BaseModel

from src.schemas.muscles import MuscleSchema
from src.schemas.utils import MeasurementUnits


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
    sets_value: int
    reps_value: int
    measurement_value: int
    measurement_unit: MeasurementUnits
    notes: Optional[str]

    class Config:
        orm_mode = True


class UpdateWorkoutOrderSchema(BaseModel):
    workout_order: list


class AddWorkoutSchema(BaseModel):
    workout_id: int


class UpdateWorkoutSchema(BaseModel):
    sets_value: Optional[int] = None
    reps_value: Optional[int] = None
    measurement_value: Optional[int] = None
    measurement_unit: Optional[MeasurementUnits] = None
    notes: Optional[str] = None


class WorkoutListSchema(BaseModel):
    workouts: list[WorkoutSchema]

    class Config:
        orm_mode = True

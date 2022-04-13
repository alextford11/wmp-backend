from enum import Enum
from typing import Optional

from pydantic import BaseModel


class MeasurementUnits(str, Enum):
    # mass
    kilogram = 'kg'
    gram = 'g'
    pound = 'lb'

    # time
    second = 's'
    minute = 'min'
    hour = 'h'

    # energy
    calorie = 'cal'

    # length
    kilometer = 'km'
    meter = 'm'
    centimeter = 'cm'
    mile = 'mi'
    yard = 'yd'
    foot = 'ft'
    inch = 'in'


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
    sets_value: int
    reps_value: int
    measurement_value: int
    measurement_unit: MeasurementUnits

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


class UpdateWorkoutSchema(BaseModel):
    sets_value: Optional[int] = None
    reps_value: Optional[int] = None
    measurement_value: Optional[int] = None
    measurement_unit: Optional[MeasurementUnits] = None


class WorkoutListSchema(BaseModel):
    workouts: list[WorkoutSchema]

    class Config:
        orm_mode = True

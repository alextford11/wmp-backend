from typing import Optional

from aenum import Enum
from pydantic import BaseModel


class LabelledEnum(Enum):
    """Enum with labels. Assumes both the value and label are strings."""

    _init_ = "value label"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # see notes below
        field_schema.pop('enum')
        field_schema.update({'choices': [{'value': choice.value, 'label': choice.label} for choice in cls]})

    @classmethod
    def validate(cls, v):
        try:
            cls(v)
        except (TypeError, ValueError):
            raise

        return v


class MeasurementUnits(LabelledEnum):
    # mass
    KILOGRAM = 'kg', 'Kilograms'
    GRAM = 'g', 'Grams'
    POUND = 'lb', 'Pounds'

    # time
    SECOND = 's', 'Seconds'
    MINUTE = 'min', 'Minutes'
    HOUR = 'h', 'Hours'

    # energy
    CALORIE = 'cal', 'Calories'

    # length
    KILOMETER = 'km', 'Kilometers'
    METER = 'm', 'Meters'
    CENTIMETER = 'cm', 'Centimeters'
    MILE = 'mi', 'Miles'
    YARD = 'yd', 'Yards'
    FOOT = 'ft', 'Feet'
    INCH = 'in', 'Inches'

    @classmethod
    def get_categories(cls) -> dict:
        return {
            'Mass': [cls.KILOGRAM, cls.GRAM, cls.POUND],
            'Time': [cls.SECOND, cls.MINUTE, cls.HOUR],
            'Energy': [cls.CALORIE],
            'Length': [cls.KILOMETER, cls.METER, cls.CENTIMETER, cls.MILE, cls.YARD, cls.FOOT, cls.INCH],
        }


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


class SelectInputOptionSchema(BaseModel):
    value: str
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

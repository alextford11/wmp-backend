from aenum import Enum


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

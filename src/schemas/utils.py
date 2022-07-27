from string import punctuation, whitespace, digits, ascii_lowercase, ascii_uppercase

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


class PasswordValidationError(ValueError):
    pass


class PasswordStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_password

    @classmethod
    def validate_password(cls, password):
        new_password = password.strip()
        min_size = 8
        if len(new_password) < min_size:
            raise PasswordValidationError(f'Password must be longer than {min_size} characters.')

        valid_chars = {'-', '_', '.', '!', '@', '#', '$', '^', '&', '(', ')'}
        invalid_chars = set(punctuation + whitespace) - valid_chars
        for char in invalid_chars:
            if char in new_password:
                raise PasswordValidationError('Password contains some invalid characters.')

        password_has_digit = False
        for char in password:
            if char in digits:
                password_has_digit = True
                break
        if not password_has_digit:
            raise PasswordValidationError('Password must contain at least one number.')

        password_has_lowercase = False
        for char in password:
            if char in ascii_lowercase:
                password_has_lowercase = True
                break
        if not password_has_lowercase:
            raise PasswordValidationError('Password must contain at least one lowercase character.')

        password_has_uppercase = False
        for char in password:
            if char in ascii_uppercase:
                password_has_uppercase = True
                break
        if not password_has_uppercase:
            raise PasswordValidationError('Password must contain at least one uppercase character.')

        return new_password

from django.core.exceptions import ValidationError


def validate_min_value_exclusive(min_value_exclusive):
    def validator(value):
        if value <= min_value_exclusive:
            raise ValidationError(f'Value must be grater than {min_value_exclusive}. Given {value}')

    return validator

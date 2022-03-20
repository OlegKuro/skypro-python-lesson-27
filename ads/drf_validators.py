from rest_framework.exceptions import ValidationError


def validate_not_equal_to(not_eq_to_value):
    def validator(value_to_validate):
        if value_to_validate == not_eq_to_value:
            raise ValidationError(f'Value cannot be equal to f{not_eq_to_value}')

    return validator

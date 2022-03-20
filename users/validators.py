from django.core.exceptions import ValidationError


def string_not_ends_with_validator(restricted_suffix: str):
    def validate(value):
        if isinstance(value, str) and value.endswith(restricted_suffix):
            raise ValidationError(f'Suffix {restricted_suffix} is forbidden!')

    return validate

from rest_framework.exceptions import ValidationError
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


def suffix_not_eq_to_validator(suffix):
    def validator(value):
        if isinstance(value, str) and value.endswith(suffix):
            raise ValidationError(f'Value cannot end with {suffix} suffix')

    return validator


def min_ages_validator(min_years):
    def validator(value: date):
        if relativedelta(datetime.now().date(), value).years < min_years:
            raise ValidationError(f'Must be older than {min_years} years old')

    return validator

from rest_framework.serializers import ModelSerializer
from users.models import User
from users.drf_validators import min_ages_validator, suffix_not_eq_to_validator


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'birth_date': {
                'validators': [min_ages_validator(User.USER_REGISTRATION_MIN_AGES)],
            },
            'email': {
                'validators': [suffix_not_eq_to_validator(User.RAMBLER_EMAIL_REGISTRATION_FORBIDDEN_SUFFIX)]
            }
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

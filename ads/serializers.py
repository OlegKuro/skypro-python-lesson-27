from rest_framework.serializers import ModelSerializer
from ads.models import Location, Category, Advertisement
from ads.drf_validators import validate_not_equal_to


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdvertisementSerializer(ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'
        extra_kwargs = {
            'is_published': {
                'validators': [validate_not_equal_to(True)],
            },
        }
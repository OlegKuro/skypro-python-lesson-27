from rest_framework.serializers import ModelSerializer
from ads.models import Location, Category, Advertisement


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
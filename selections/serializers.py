from selections.models import Selection
from rest_framework import serializers
from ads.serializers import AdvertisementSerializer


class SelectionBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = [
            'id',
            'name',
        ]


class SelectionRetrieveView(SelectionBaseSerializer):
    items = AdvertisementSerializer(many=True)

    class Meta(SelectionBaseSerializer.Meta):
        fields = SelectionBaseSerializer.Meta.fields + [
            'items',
        ]


class SelectionCreateUpdateView(SelectionBaseSerializer):
    class Meta(SelectionBaseSerializer.Meta):
        fields = SelectionBaseSerializer.Meta.fields + [
            'items',
        ]

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

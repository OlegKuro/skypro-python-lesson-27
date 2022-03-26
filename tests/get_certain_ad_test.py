import pytest
from ads.factories import AdvertisementFactory
from ads.models import Advertisement
from ads.views import AdRUDView
from rest_framework import status


@pytest.mark.django_db
def test_get_certain_ad(client, advertisement_factory: AdvertisementFactory, member_token):
    ad: Advertisement = advertisement_factory.create()

    response = client.get(f'/ad/{ad.pk}/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response = client.get(f'/ad/{ad.pk}/', HTTP_AUTHORIZATION=f'Bearer {member_token}')
    assert response.status_code == status.HTTP_200_OK
    serializer = AdRUDView.serializer_class

    assert serializer(ad).data == response.json()

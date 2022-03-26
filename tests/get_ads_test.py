import pytest
from rest_framework import status
from ads.views import AdsListCreate as ListView


@pytest.mark.django_db
@pytest.mark.parametrize('page', range(1, 5))
def test_get_ads(client, advertisement_factory, page):
    ads = advertisement_factory.create_batch(20)
    response = client.get(f'/ad/?page={page}')
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data['count'] == 20
    assert len(data['results']) == 10

    serializer = ListView.serializer_class

    assert serializer(ads[0:10], many=True).data == data['results']



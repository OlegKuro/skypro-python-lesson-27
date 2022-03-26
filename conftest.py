import pytest
from rest_framework import status
from users.models import User
from ads.models import Advertisement
from datetime import datetime
from pytest_factoryboy import register
from ads.factories import AdvertisementFactory

register(AdvertisementFactory)


@pytest.fixture()
@pytest.mark.django_db
def user_member_fixture(django_user_model):
    username = "oleg"
    password = "qwerty"

    user = django_user_model.objects.create_user(username=username, password=password, role=User.ROLE_MEMBER,
                                                 birth_date=datetime.now(), email='lel-top@kek.cock')
    return user


@pytest.fixture()
@pytest.mark.django_db
def member_token(client, django_user_model):
    username = "oleg2"
    password = "qwerty2"

    django_user_model.objects.create_user(username=username, password=password, role=User.ROLE_MEMBER,
                                                 birth_date=datetime.now())
    response = client.post(
        "/users/login/",
        {"username": "oleg2", "password": "qwerty2"},
        format='json'
    )
    return response.data["access"]


@pytest.fixture()
@pytest.mark.django_db
def ad_fixture(client, member_token, user_member_fixture):
    body = {'name': '123456789012', 'price': 1, 'description': '', 'is_published': False, 'author': user_member_fixture}
    ad = Advertisement.objects.create(**body)
    return ad


@pytest.fixture()
def create_ad_test_cases_provider(member_token):
    return (
        ('unauthorized request', {}, status.HTTP_401_UNAUTHORIZED, ''),
        ('empty request', {}, status.HTTP_400_BAD_REQUEST, member_token),
        ('good request', {'name': '123456789012', 'price': 1, 'description': '', 'is_published': False, 'author': 1},
         status.HTTP_201_CREATED, member_token),
        ('name too short', {'name': 'test', 'price': 1, 'description': '', 'is_published': False, 'author': 1},
         status.HTTP_400_BAD_REQUEST, member_token),
        ('cannot create published',
         {'name': '123456789012', 'price': 1, 'description': '123', 'is_published': True, 'author': 1},
         status.HTTP_400_BAD_REQUEST, member_token),
        ('price must be greater than or equal to 0',
         {'name': '123456789012', 'price': -1, 'description': '123', 'is_published': False, 'author': 1},
         status.HTTP_400_BAD_REQUEST, member_token),
    )


@pytest.fixture()
def create_selection_test_cases_provider(member_token, ad_fixture):
    return (
        ('unauthorized request', {}, status.HTTP_401_UNAUTHORIZED, ''),
        ('empty selection', {'name': 'test_selection', 'items': []}, status.HTTP_400_BAD_REQUEST, member_token),
        ('not empty selection', {'name': 'test_selection', 'items': [ad_fixture.id]}, status.HTTP_201_CREATED,
         member_token),
    )

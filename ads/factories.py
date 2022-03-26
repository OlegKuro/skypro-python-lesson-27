import factory.faker
from ads.models import Advertisement


class AdvertisementFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f'Advertisement number {n}')
    author = None
    price = 123
    description = factory.Sequence(lambda n: f'Description number {n}')
    is_published = False
    image = None
    category = None

    class Meta:
        model = Advertisement

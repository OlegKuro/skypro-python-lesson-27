from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator


class Advertisement(models.Model):
    name = models.TextField(null=False, blank=False, validators=[MinLengthValidator(10)])
    author = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.CASCADE,
                               related_name='advertisements')
    price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField(null=True, blank=True)
    is_published = models.BooleanField()
    image = models.ImageField(upload_to='images', null=True, blank=True)
    category = models.ForeignKey(to='Category', blank=True, null=True, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'Объява'
        verbose_name_plural = 'Объявы'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=10, unique=True, validators=[MinLengthValidator(5)])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=20, decimal_places=6)
    lng = models.DecimalField(max_digits=20, decimal_places=6)

    class Meta:
        unique_together = ['name', 'lat', 'lng']
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.name

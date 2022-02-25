from django.db import models


class Advertisement(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.CASCADE)
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    is_published = models.BooleanField()
    image = models.ImageField(upload_to='images', null=True, blank=True)
    category = models.ForeignKey(to='Category', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Объява'
        verbose_name_plural = 'Объявы'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

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

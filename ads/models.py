from django.db import models


class Advertisement(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=100)
    is_published = models.BooleanField()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
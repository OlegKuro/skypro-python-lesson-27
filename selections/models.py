from django.db import models
from users.models import User
from ads.models import Advertisement


class Selection(models.Model):
    name = models.CharField(max_length=1000)
    author = models.ForeignKey(User, related_name='selections', on_delete=models.CASCADE)
    items = models.ManyToManyField(Advertisement, related_name='selections')

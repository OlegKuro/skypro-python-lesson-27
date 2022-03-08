from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_MODERATOR = 'moderator'
    ROLE_MEMBER = 'member'
    ROLES = (
         (ROLE_ADMIN, 'admin'),
         (ROLE_MODERATOR, 'moderator'),
         (ROLE_MEMBER, 'member'),
    )
    locations = models.ManyToManyField('ads.Location', null=True, blank=True)
    role = models.CharField(max_length=100, choices=ROLES, default=ROLE_MEMBER)

    class Meta:
        verbose_name = 'Юзер'
        verbose_name_plural = 'Юзеры'
        ordering = ('username',)

    def __str__(self):
        return self.username

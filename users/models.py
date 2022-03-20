from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    RAMBLER_EMAIL_REGISTRATION_FORBIDDEN_SUFFIX = 'rambler.ru'
    USER_REGISTRATION_MIN_AGES = 9

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
    birth_date = models.DateField()
    email = models.EmailField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Юзер'
        verbose_name_plural = 'Юзеры'
        ordering = ('username',)

    def __str__(self):
        return self.username

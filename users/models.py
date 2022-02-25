from django.db import models


class User(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_MODERATOR = 'moderator'
    ROLE_MEMBER = 'member'
    ROLES = (
        (ROLE_ADMIN, 'admin'),
        (ROLE_MODERATOR, 'moderator'),
        (ROLE_MEMBER, 'member')
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=ROLES)
    age = models.SmallIntegerField()
    location = models.ForeignKey('ads.Location', null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Юзер'
        verbose_name_plural = 'Юзеры'

    def __str__(self):
        return self.username

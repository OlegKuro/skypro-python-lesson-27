from django.db import models


class User(models.Model):
    ROLES = (
        ('admin', 'admin'),
        ('moderator', 'moderator'),
        ('member', 'member')
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=ROLES, default='member')
    age = models.SmallIntegerField()
    locations = models.ManyToManyField('ads.Location')

    class Meta:
        verbose_name = 'Юзер'
        verbose_name_plural = 'Юзеры'
        ordering = ('username',)

    def __str__(self):
        return self.username

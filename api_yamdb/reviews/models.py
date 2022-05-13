from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE,
        default='user',
        verbose_name='Роль пользователя',
    )
    confirmation_code = models.CharField(max_length=15)

    USERNAME_FIELDS = 'username'

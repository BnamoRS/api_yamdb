from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'UR'
    MODERATOR = 'MD'
    ADMIN = 'AD'
    ROLE = [
        ('UR', 'user'),
        ('MD', 'moderator'),
        ('AD', 'admin'),
    ]
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=2,
        choices=ROLE,
        default='UR',
        verbose_name='Роль пользователя',
    )
    confirmation_code = models.CharField(max_length=15)

    USERNAME_FIELDS = 'username'

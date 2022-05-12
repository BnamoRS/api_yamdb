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
        unique=True,
        verbose_name='Роль пользователя',
    )


class Category(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.TextField(max_length=64)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Titles(models.Model):
    name = models.TextField(max_length=64)
    year = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=None, null=True, blank=True)
    # description = models.TextField(max_length=200)
    # genre = models.ForeignKey(Genre, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, models.CASCADE)

    def __str__(self):
        return self.name

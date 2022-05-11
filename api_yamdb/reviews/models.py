from django.contrib.auth.models import AbstractUser
from django.db import models

SCORE_CHOICE = [i for i in range(1, 11)]


class Title(models.Model):
    pass


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


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(choices=SCORE_CHOICE)
    pub_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

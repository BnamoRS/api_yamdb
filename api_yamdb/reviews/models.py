from tabnanny import verbose
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Title(models.Model):
    pass


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

    class Meta: 
        verbose_name = 'Пользователь' 
        verbose_name_plural = 'Пользователи'


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )


    class Meta: 
        verbose_name = 'Отзыв' 
        verbose_name_plural = 'Отзывы' 


    def __str__(self):
        return self.text[:15]

class Comment(models.Model):
    text = models.TextField()
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )


    class Meta: 
        verbose_name = 'Комментарий' 
        verbose_name_plural = 'Комментарии' 

    def __str__(self):
        return self.text[:15]

from unicodedata import category
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

ROLE_LIST = [
    ('user', 'пользователь'),
    ('admin', 'администратор'),
    ('moderator', 'модератор')
]


class User(AbstractUser):
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(max_length=20, choices=ROLE_LIST, default='user')


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ManyToManyField(
        Genre, related_name='titles', blank=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles', null=True
    )
    description = models.TextField()
    year = models.IntegerField()


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review')
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

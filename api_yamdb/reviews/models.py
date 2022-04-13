from pyexpat import model
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
    REQUIRED_FIELD = ['username', 'email']


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200)
    genre = models.ManyToManyField(
        Genre, through='TitleGenre'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles', blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    year = models.IntegerField()


class TitleGenre(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.SET_NULL, blank=True, null=True)
    genre_id = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True)


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

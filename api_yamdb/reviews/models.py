from tabnanny import verbose
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
CHOICES = (
    (USER, 'user'),
    (ADMIN, 'admin'),
    (MODERATOR, 'moderator'),
)


class User(AbstractUser):
    bio = models.TextField('Биография', blank=True,)
    role = models.CharField(max_length=20, choices=CHOICES, default=USER)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    confirmation_code = models.CharField(max_length=10, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    REQUIRED_FIELD = ['username', 'email']

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email', 'username'],
                                    name='unique_user')
        ]
        ordering = ['username']

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель Category"""
    name = models.CharField(max_length=256, verbose_name='Название категории')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель Genre"""
    name = models.CharField(max_length=256, verbose_name='Название жанра')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель Title"""
    name = models.CharField(max_length=200, verbose_name='Название произведения')
    genre = models.ManyToManyField(
        Genre, blank=True, verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', null=True,
        verbose_name='Категория'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    year = models.IntegerField(verbose_name='Год создания')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name



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
        ordering = ['-pub_date']

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

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text

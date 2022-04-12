from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_LIST = [
    ('user', 'пользователь'),
    ('admin', 'администратор'),
    ('moderator', 'модератор')
]
class User(AbstractUser):
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(max_length=20, choices=ROLE_LIST, default='user')
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    """User model."""

    email = models.EmailField(
        max_length=settings.MAX_EMAIL_LENGTH,
        verbose_name='email',
        unique=True)
    username = models.CharField(
        verbose_name='Псевдоним',
        max_length=settings.MAX_USERS_NAMES_LENGTH,
        unique=True,
        validators=(
            UnicodeUsernameValidator(),
        ))

    REQUIRED_FIELDS = ('email',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

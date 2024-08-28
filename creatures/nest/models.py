from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Nest(models.Model):
    """Nest model."""

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='nests',
        verbose_name='Хозяин')
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.MAX_CREATURE_NAMES_LENGTH
    )
    new_creature_birth_process = models.IntegerField(
        verbose_name='Процесс рождения нового существа',
        default=0
    )
    area = models.ForeignKey(
        'area.Area',
        on_delete=models.SET_NULL,
        null=True,
        related_name='nests',
        verbose_name='Территория'
    )

    class Meta:
        verbose_name = 'Гнездо'
        verbose_name_plural = 'Гнезда'

    def __str__(self):
        return f'Гнездо {self.name} пользователя {self.owner.username}'

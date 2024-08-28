from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Beast(models.Model):
    """Beast model."""

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='beasts',
        verbose_name='Хозяин')
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.MAX_CREATURE_NAMES_LENGTH
    )
    description = models.TextField(verbose_name='Описание')
    health = models.IntegerField(
        verbose_name='Здоровье',
        default=100
    )
    attack = models.IntegerField(
        verbose_name='Атака',
        default=10
    )
    defense = models.IntegerField(
        verbose_name='Защита',
        default=0
    )
    experience = models.IntegerField(
        verbose_name='Опыт',
        default=0
    )
    nest = models.ForeignKey(
        'nest.Nest',
        on_delete=models.PROTECT,
        related_name='beasts',
        verbose_name='Гнездо'
    )

    class Meta:
        verbose_name = 'Создание'
        verbose_name_plural = 'Создания'
        constraints = (
            models.UniqueConstraint(
                name='beast_name_owner_unique',
                fields=('owner', 'name')
            ),
        )

    def __str__(self):
        return f'Чудовище {self.name} созданное {self.owner.username}'

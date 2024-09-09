from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
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

    @property
    def in_nest(self):
        return not bool(
            cache.get(
                settings.BEAST_ACTION_KEY.format(beast=self),
                None))

    def increase_experience(self, amount):
        self.experience += amount
        self.save()

    def decrease_experience(self, amount):
        self.experience -= amount
        self.save()

    def decrease_health(self, amount):
        self.health -= amount
        self.save()

    def set_health(self, amount):
        self.health = amount
        self.save()

    def level_up(self, ability_name):
        self.decrease_experience(settings.NEW_LEVEL_EXPERIENTS)
        setattr(
            self,
            ability_name,
            getattr(self, ability_name) +
            settings.LVL_UP_ABILITY_NAME_VALUE[ability_name])
        self.save()

    def __str__(self):
        return f'Чудовище {self.name} созданное {self.owner.username}'

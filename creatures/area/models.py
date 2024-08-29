from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Area(models.Model):
    """Area model."""

    name = models.CharField(
        verbose_name='Название',
        max_length=settings.MAX_AREA_NAMES_LENGTH,
        unique=True
    )
    description = models.TextField(verbose_name='Описание')
    attacker_attack_impact = models.IntegerField(
        verbose_name='Влияние на атаку атакующей стороны', default=0)
    attacker_defense_impact = models.IntegerField(
        verbose_name='Влияние на защиту атакующей стороны', default=0)
    defender_attack_impact = models.IntegerField(
        verbose_name='Влияние на атаку защищающейся стороны', default=0)
    defender_defense_impact = models.IntegerField(
        verbose_name='Влияние на защиту защищающейся стороны', default=0)

    class Meta:
        verbose_name = 'Зона'
        verbose_name_plural = 'Зоны'

    def __str__(self):
        return f'{self.name}'

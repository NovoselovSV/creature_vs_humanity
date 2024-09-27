from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Nest
from area.models import Area

User = get_user_model()


@receiver(post_save, sender=User)
def add_first_nest(sender, instance, created, **kwargs):
    if not created:
        return
    if not Area.objects.count():
        Area(name=settings.FIRST_AREA_NAME,
             description=settings.FIRST_AREA_DESCRIPTION).save()
    Nest(
        owner=instance,
        name=settings.FIRST_NEST_NAME,
        new_creature_birth_process=settings.BIRTH_PROCESS_TO_APPEAR,
        area=Area.objects.all().first()).save()

from django.contrib.auth import get_user_model
from django.core.cache import cache

from celery import shared_task

from .models import Nest
from beast.models import Beast

User = get_user_model()


@shared_task()
def create_creature(nest_id, new_creature_data, key):
    owner_id = new_creature_data.pop('owner')
    if not User.objects.filter(id=owner_id).exists():
        return
    if not Nest.objects.filter(id=nest_id).exists():
        return
    if Beast.objects.filter(
            owner_id=owner_id,
            name=new_creature_data['name']).exists():
        return
    Beast.objects.create(
        **new_creature_data,
        nest_id=nest_id,
        owner_id=owner_id)
    cache.delete(key)

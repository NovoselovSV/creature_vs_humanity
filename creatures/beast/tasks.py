from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache

from celery import shared_task

from .models import Beast
from nest.models import Nest

User = get_user_model()


@shared_task()
def obtain_resources_for_nest(beast_id, key):
    beast = get_object_or_none(Beast, beast_id)
    if not beast:
        return
    beast.nest.inrease_birth_process(settings.EARNING_BIRTH_PROCESS)
    cache.delete(key)


@shared_task()
def obtain_experience(beast_id, key):
    beast = get_object_or_none(Beast, beast_id)
    if not beast:
        return
    beast.increase_experience(settings.EARNING_EXPERIENCE)
    cache.delete(key)


@shared_task()
def create_nest(beast_id, owner_id, nest_data, key):
    beast = get_object_or_none(Beast, beast_id)
    if not beast:
        return
    if not get_object_or_none(User, owner_id):
        return
    area = nest_data.pop('area')
    new_nest = Nest.objects.create(
        **nest_data,
        owner_id=owner_id,
        area_id=area['id'])
    beast.nest = new_nest
    beast.save()
    cache.delete(key)


def get_object_or_none(model_cls, object_id):
    try:
        return model_cls.objects.get(id=object_id)
    except model_cls.DoesNotExist:
        return

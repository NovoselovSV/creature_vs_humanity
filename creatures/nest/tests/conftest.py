from functools import wraps
from django.test.client import Client
from django.core.cache import cache

from celery.result import AsyncResult
from celery.app.control import Control
from rest_framework.viewsets import reverse
import pytest

from area.models import Area
from creatures import settings
from creatures.celery import app
from nest.models import Nest

CREATED_OWNER_EMAIL = 'owner@mail.com'
CREATED_OWNER_USERNAME = 'owner_username'
CREATED_NOT_OWNER_EMAIL = 'not_owner@mail.com'
CREATED_NOT_OWNER_USERNAME = 'not_owner_username'
CREATED_NEST_NAME = 'Nest name'
CREATED_NOT_OWNER_NEST_NAME = 'Nest name for not owner'
CREATED_NEST_B_PROCESS = settings.BIRTH_PROCESS_TO_APPEAR
NEST_AREA_NAME = 'Nest area name'
NEST_AREA_DESCRIPTION = 'Nest area description'
pytest_plugins = ('pytest_general.general_fixtures',)


@pytest.fixture
def created_owner(django_user_model):
    return django_user_model.objects.create(
        email=CREATED_OWNER_EMAIL,
        username=CREATED_OWNER_USERNAME)


@pytest.fixture
def created_owner_client(created_owner):
    client = Client()
    client.force_login(created_owner)
    return client


@pytest.fixture
def created_not_owner(django_user_model):
    return django_user_model.objects.create(
        email=CREATED_NOT_OWNER_EMAIL,
        username=CREATED_NOT_OWNER_USERNAME)


@pytest.fixture
def created_not_owner_client(created_not_owner):
    client = Client()
    client.force_login(created_not_owner)
    return client


@pytest.fixture
def created_nest_area(django_user_model):
    return Area.objects.create(
        name=NEST_AREA_NAME,
        description=NEST_AREA_DESCRIPTION)


@pytest.fixture
def created_nest(created_owner, created_nest_area):
    return Nest.objects.create(
        owner=created_owner,
        name=CREATED_NEST_NAME,
        new_creature_birth_process=CREATED_NEST_B_PROCESS,
        area=created_nest_area)


@pytest.fixture
def created_not_owner_nest(created_not_owner, created_nest_area):
    return Nest.objects.create(
        owner=created_not_owner,
        name=CREATED_NOT_OWNER_NEST_NAME,
        new_creature_birth_process=CREATED_NEST_B_PROCESS,
        area=created_nest_area)


@pytest.fixture
def delete_redis_key_nest(created_nest):
    yield
    key = settings.BIRTH_KEY.format(nest=created_nest)
    celery_key = cache.get(key)
    Control(app).revoke(celery_key, terminate=True)
    cache.delete(key)


@pytest.fixture
def url_nest(created_nest):
    return reverse('nest:nest-detail', args=(created_nest.id,))


@pytest.fixture
def url_nests():
    return reverse('nest:nest-list')


@pytest.fixture
def url_birth(created_nest):
    return reverse('nest:nest-birth', args=(created_nest.id,))

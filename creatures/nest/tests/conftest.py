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

pytest_plugins = ('pytest_general.general_fixtures',)


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

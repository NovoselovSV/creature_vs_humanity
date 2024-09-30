import hashlib

from django.core.cache import cache
from django.urls import reverse

import pytest

from celery.app.control import Control
from core.shortcuts import get_bytes_from_stringed
from creatures import settings
from creatures.celery import app

pytest_plugins = ('pytest_general.general_fixtures',)


@pytest.fixture
def url_beast(created_owner_beast):
    return reverse('beast:beast-detail', args=(created_owner_beast.id,))


@pytest.fixture
def url_beasts():
    return reverse('beast:beast-list')


@pytest.fixture
def url_get_resources_for_nest(created_owner_beast):
    return reverse(
        'beast:beast-get-resources-for-nest',
        args=(created_owner_beast.id,
              ))


@pytest.fixture
def url_get_stronger(created_owner_beast):
    return reverse(
        'beast:beast-get-stronger',
        args=(created_owner_beast.id,
              ))


@pytest.fixture
def url_attack(created_owner_beast):
    return reverse(
        'beast:beast-attack',
        args=(created_owner_beast.id,
              ))


@pytest.fixture
def url_create_new_nest(created_owner_beast):
    return reverse(
        'beast:beast-create-new-nest',
        args=(created_owner_beast.id,
              ))


@pytest.fixture
def url_level_up(created_owner_beast):
    return reverse(
        'beast:beast-level-up',
        args=(created_owner_beast.id,
              ))


@pytest.fixture
def url_defense(created_owner_beast):
    return reverse(
        'beast:beast-defense',
        args=(created_owner_beast.id,
              ))


@pytest.fixture
def beast_key(created_owner_beast):
    return settings.BEAST_ACTION_KEY.format(beast=created_owner_beast)


@pytest.fixture
def delete_redis_n_celery_key_beast(created_owner_beast, beast_key):
    yield
    celery_key = cache.get(beast_key)
    Control(app).revoke(celery_key, terminate=True)
    cache.delete(beast_key)


@pytest.fixture
def humans_group_data(group_members):
    hashed_group_parametrs = hashlib.sha256()
    for member in group_members:
        hashed_group_parametrs.update(
            get_bytes_from_stringed(member.get('id', 0)))
        hashed_group_parametrs.update(
            get_bytes_from_stringed(member.get('health', 0)))
        hashed_group_parametrs.update(
            get_bytes_from_stringed(member.get('attack', 0)))
    hashed_group_parametrs.update(
        get_bytes_from_stringed(
            settings.HUMANS_SALT))
    return {'members': group_members,
            'signature': hashed_group_parametrs.hexdigest()}


@pytest.fixture
def attack_response_data():
    experience = 100
    health = 200
    hashed_beast_parametrs = hashlib.sha256()
    hashed_beast_parametrs.update(
        get_bytes_from_stringed(health))
    hashed_beast_parametrs.update(
        get_bytes_from_stringed(experience))
    hashed_beast_parametrs.update(
        get_bytes_from_stringed(settings.BEAST_SALT))
    return {'experience': experience,
            'health': health,
            'signature': hashed_beast_parametrs.hexdigest()}

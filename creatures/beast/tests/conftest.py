from django.utils.functional import wraps
from django.urls import reverse

import pytest

from beast.models import Beast

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

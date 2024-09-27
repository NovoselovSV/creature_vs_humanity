from functools import wraps

from django.test.client import Client
from django.urls import reverse

import pytest

pytest_plugins = ('pytest_general.general_fixtures',)


@pytest.fixture
def url_user(created_owner):
    return reverse('core:users-detail', args=(created_owner.id,))


@pytest.fixture
def url_users():
    return reverse('core:users-list')


@pytest.fixture
def url_me():
    return reverse('core:users-me')

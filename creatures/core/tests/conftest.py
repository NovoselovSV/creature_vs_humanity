from functools import wraps

from django.test.client import Client
from django.urls import reverse
import pytest

CREATED_USER_EMAIL = 'some@mail.com'
CREATED_USER_USERNAME = 'some_username'
pytest_plugins = ('pytest_general.general_fixtures',)


@pytest.fixture
def created_user(django_user_model):
    return django_user_model.objects.create(
        email=CREATED_USER_EMAIL,
        username=CREATED_USER_USERNAME)


@pytest.fixture
def url_user(created_user):
    return reverse('core:users-detail', args=(created_user.id,))


@pytest.fixture
def url_users():
    return reverse('core:users-list')


@pytest.fixture
def url_me():
    return reverse('core:users-me')


@pytest.fixture
def created_client(created_user):
    client = Client()
    client.force_login(created_user)
    return client

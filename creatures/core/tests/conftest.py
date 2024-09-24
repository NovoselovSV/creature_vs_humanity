from functools import wraps

from django.test.client import Client
from django.urls import reverse
import pytest

CREATED_USER_EMAIL = 'some@mail.com'
CREATED_USER_USERNAME = 'some_username'


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


@pytest.fixture
def user_diff_expect(db, request, django_user_model):
    def fabric(func):
        @wraps(func)
        def wrapper():
            user_count_before = django_user_model.objects.count()
            func()
            user_count_after = django_user_model.objects.count()
            assert (
                user_count_after
                - user_count_before == request.param)
        return wrapper
    return fabric

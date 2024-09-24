import pytest
from pytest_lazy_fixtures import lf

from core.tests import conftest


@pytest.mark.parametrize(
    'url, http_client', (
        (lf('url_user'), lf('client')),
        (lf('url_me'), lf('created_client')),
    )
)
def test_user_has_content(url, http_client):
    response = http_client.get(url)
    response_json = response.json()
    assert 'id' in response_json
    assert 'email' in response_json
    assert 'username' in response_json
    assert 'password' not in response_json


@pytest.mark.parametrize(
    'url, http_client', (
        (lf('url_user'), lf('client')),
        (lf('url_me'), lf('created_client')),
    )
)
def test_area_content(url, http_client):
    response = http_client.get(url)
    response_json = response.json()
    assert response_json['email'] == conftest.CREATED_USER_EMAIL
    assert (response_json['username']
            == conftest.CREATED_USER_USERNAME)

from pytest_lazy_fixtures import lf
from rest_framework import status
import pytest


@pytest.mark.parametrize(
    'url', (
        lf('url_beast'),
        lf('url_beasts'),
    )
)
def test_beast_endpoints_availability(db, url, created_owner_client):
    response = created_owner_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    'url, method', (
        (lf('url_beast'), 'get'),
        (lf('url_beasts'), 'get'),
        (lf('url_get_resources_for_nest'), 'patch'),
        (lf('url_get_stronger'), 'patch'),
        (lf('url_attack'), 'post'),
        (lf('url_create_new_nest'), 'post'),
        (lf('url_level_up'), 'patch'),
    )
)
def test_unauth_nests_endpoints_availability(db, url, client, method):
    response = getattr(client, method)(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    'url, method', (
        (lf('url_beast'), 'get'),
        (lf('url_get_resources_for_nest'), 'patch'),
        (lf('url_get_stronger'), 'patch'),
        (lf('url_attack'), 'post'),
        (lf('url_create_new_nest'), 'post'),
        (lf('url_level_up'), 'patch'),
    )
)
def test_unowner_beast_endpoints_availability(
        url, created_not_owner_client, method):
    response = getattr(created_not_owner_client, method)(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

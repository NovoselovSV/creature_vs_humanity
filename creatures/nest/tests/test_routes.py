import pytest
from pytest_lazy_fixtures import lf
from rest_framework import status


@pytest.mark.parametrize(
    'url', (
        lf('url_nest'),
        lf('url_nests'),
    )
)
def test_nests_endpoints_availability(url, created_owner_client):
    response = created_owner_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_birth_endpoint_availability(
        url_birth,
        created_owner_client,
        delete_redis_key_nest):
    response = created_owner_client.post(
        url_birth,
        content_type='application/json',
        data={
            'name': 'Name new beast',
            'description': 'Description new beast'})
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.parametrize(
    'url, method', (
        (lf('url_nest'), 'get'),
        (lf('url_nests'), 'get'),
        (lf('url_birth'), 'post'),
    )
)
def test_unauth_nests_endpoints_availability(db, url, client, method):
    response = getattr(client, method)(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize(
    'url, status, method', (
        (lf('url_nest'), status.HTTP_404_NOT_FOUND, 'get'),
        (lf('url_nests'), status.HTTP_200_OK, 'get'),
        (lf('url_birth'), status.HTTP_404_NOT_FOUND, 'post'),
    )
)
def test_unowner_nests_endpoints_availability(
        url, created_not_owner_client, status, method):
    response = getattr(created_not_owner_client, method)(url)
    assert response.status_code == status

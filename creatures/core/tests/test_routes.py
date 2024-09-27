from pytest_lazy_fixtures import lf
from rest_framework import status
import pytest


@pytest.mark.parametrize(
    'url, http_client', (
        (lf('url_users'), lf('client')),
        (lf('url_user'), lf('client')),
        (lf('url_me'), lf('created_owner_client')),
    )
)
def test_core_endpoints_availability(db, url, http_client):
    response = http_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_unauth_create_user_availability(db, client, url_users):
    response = client.post(
        url_users,
        content_type='application/json',
        data={
            'email': 'some@thing.net',
            'username': 'someone',
            'password': 'S0meStr0ngPassw0rd'})
    assert response.status_code == status.HTTP_201_CREATED


def test_unauth_me_availability(db, client, url_me):
    response = client.get(url_me)
    assert response.status_code == status.HTTP_403_FORBIDDEN

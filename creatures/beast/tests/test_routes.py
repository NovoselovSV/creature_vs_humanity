from django.core.cache import cache

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
    'url', (
        lf('url_get_resources_for_nest'),
        lf('url_get_stronger'),
    )
)
def test_patch_n_wait_beast_endpoints_availability(
        db, url, created_owner_client, delete_redis_n_celery_key_beast):
    response = created_owner_client.patch(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    'level_up_data', (
        {'ability_name': 'attack'},
        {'ability_name': 'defense'},
        {'ability_name': 'health'}
    )
)
def test_level_up_beast_endpoints_availability(
        db,
        url_level_up,
        created_owner_client,
        level_up_data):
    response = created_owner_client.patch(
        url_level_up,
        content_type='application/json',
        data=level_up_data)
    assert response.status_code == status.HTTP_200_OK


def test_defense_beast_endpoint_availability(
        db, url_defense, beast_busy, client, beast_key, humans_group_data):
    response = client.post(
        url_defense,
        content_type='application/json',
        data=humans_group_data)
    assert response.status_code == status.HTTP_201_CREATED


def test_attack_beast_endpoint_availability(
        db,
        url_attack,
        created_owner_client,
        requests_mock,
        humans_defense_get_url,
        attack_response_data):
    attacked_group_id = 0
    requests_mock.post(
        humans_defense_get_url(attacked_group_id),
        status_code=status.HTTP_201_CREATED,
        json=attack_response_data)
    response = created_owner_client.post(
        url_attack,
        content_type='application/json',
        data={'id': attacked_group_id})
    assert response.status_code == status.HTTP_201_CREATED


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
def test_unauth_beast_endpoints_availability(db, url, client, method):
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

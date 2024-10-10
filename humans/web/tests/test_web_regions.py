import pytest
from fastapi import status


@pytest.mark.parametrize('url', ('/regions/', '/regions/{region_id}'))
def test_regions_get_endpoints_availability(
        unauth_client, url, get_temporal_region):
    response = unauth_client.get(url.format(region_id=get_temporal_region.id))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize('url', ('/regions/', '/regions/{region_id}'))
def test_regions_get_endpoints_content(
        unauth_client,
        url,
        check_compare_object_with_response,
        get_temporal_region):
    response = unauth_client.get(url.format(region_id=get_temporal_region.id))
    assert response.status_code == status.HTTP_200_OK
    check_compare_object_with_response(response.json(), get_temporal_region)


def test_regions_get_wrong_id(
        unauth_client, get_temporal_region):
    response = unauth_client.get('/regions/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND

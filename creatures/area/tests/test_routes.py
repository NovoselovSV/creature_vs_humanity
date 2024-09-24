import pytest

from rest_framework import status
from pytest_lazy_fixtures import lf


@pytest.mark.parametrize(
    'url', (
        lf('url_area'),
        lf('url_areas'),
    )
)
def test_pages_availability(client, url):
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

from functools import wraps
from django.urls import reverse
import pytest


@pytest.fixture
def url_area(created_area):
    return reverse('area:area-detail', args=(created_area.id,))


@pytest.fixture
def url_areas(created_area):
    return reverse('area:area-list')

from django.utils.functional import wraps
import pytest

from beast.models import Beast

CREATED_BEAST_NAME = 'New beast'
CREATED_BEAST_DESCRIPTION = 'New beast description'


@pytest.fixture
def beast_diff_expect(db, request):
    def fabric(func):
        @wraps(func)
        def wrapper():
            beast_count_before = Beast.objects.count()
            func()
            beast_count_after = Beast.objects.count()
            assert (
                beast_count_after
                - beast_count_before == request.param)
        return wrapper
    return fabric


@pytest.fixture
def created_beast(created_owner, created_nest):
    return Beast.objects.create(
        owner=created_owner,
        name=CREATED_BEAST_NAME,
        description=CREATED_BEAST_DESCRIPTION,
        nest=created_nest)

from django.utils.functional import wraps
import pytest


@pytest.fixture
def make_diff_expect(db, request):
    def fabric(func):
        @wraps(func)
        def wrapper(db_model):
            count_before = db_model.objects.count()
            func()
            count_after = db_model.objects.count()
            assert (
                count_after
                - count_before == request.param)
        return wrapper
    return fabric

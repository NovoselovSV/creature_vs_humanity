from functools import wraps
from django.urls import reverse
import pytest

from area.models import Area

AREA_NAME = 'Название зоны'
AREA_DESCRIPTION = 'Описание зоны'
AREA_ATTACKER_ATTACK_IMPACT = 1
AREA_ATTACKER_DEFENSE_IMPACT = 2
AREA_DEFENDER_ATTACK_IMPACT = 3
AREA_DEFENDER_DEFENSE_IMPACT = 4


@pytest.fixture
def created_area(db):
    return Area.objects.create(
        name=AREA_NAME,
        description=AREA_DESCRIPTION,
        attacker_attack_impact=AREA_ATTACKER_ATTACK_IMPACT,
        attacker_defense_impact=AREA_ATTACKER_DEFENSE_IMPACT,
        defender_attack_impact=AREA_DEFENDER_ATTACK_IMPACT,
        defender_defense_impact=AREA_DEFENDER_DEFENSE_IMPACT)


@pytest.fixture
def url_area(created_area):
    return reverse('area:area-detail', args=(created_area.id,))


@pytest.fixture
def url_areas(created_area):
    return reverse('area:area-list')


@pytest.fixture
def area_diff_expect(db, request):
    def fabric(func):
        @wraps(func)
        def wrapper():
            area_count_before = Area.objects.count()
            func()
            area_count_after = Area.objects.count()
            assert (
                area_count_after
                - area_count_before == request.param)
        return wrapper
    return fabric

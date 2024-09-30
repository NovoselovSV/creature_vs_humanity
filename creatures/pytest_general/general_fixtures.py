from django.test.client import Client
from django.utils.functional import wraps
import pytest

from beast.models import Beast

from . import constants
from area.models import Area
from nest.models import Nest


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


@pytest.fixture
def created_area(db):
    return Area.objects.create(
        name=constants.AREA_NAME,
        description=constants.AREA_DESCRIPTION,
        attacker_attack_impact=constants.AREA_ATTACKER_ATTACK_IMPACT,
        attacker_defense_impact=constants.AREA_ATTACKER_DEFENSE_IMPACT,
        defender_attack_impact=constants.AREA_DEFENDER_ATTACK_IMPACT,
        defender_defense_impact=constants.AREA_DEFENDER_DEFENSE_IMPACT)


@pytest.fixture
def created_owner(django_user_model):
    return django_user_model.objects.create(
        email=constants.CREATED_OWNER_EMAIL,
        username=constants.CREATED_OWNER_USERNAME)


@pytest.fixture
def created_owner_client(created_owner):
    client = Client()
    client.force_login(created_owner)
    return client


@pytest.fixture
def created_not_owner(django_user_model):
    return django_user_model.objects.create(
        email=constants.CREATED_NOT_OWNER_EMAIL,
        username=constants.CREATED_NOT_OWNER_USERNAME)


@pytest.fixture
def created_not_owner_client(created_not_owner):
    client = Client()
    client.force_login(created_not_owner)
    return client


@pytest.fixture
def created_nest(created_owner, created_area):
    return Nest.objects.create(
        owner=created_owner,
        name=constants.CREATED_NEST_NAME,
        new_creature_birth_process=constants.CREATED_NEST_B_PROCESS,
        area=created_area)


@pytest.fixture
def created_not_owner_nest(created_not_owner, created_area):
    return Nest.objects.create(
        owner=created_not_owner,
        name=constants.CREATED_NOT_OWNER_NEST_NAME,
        new_creature_birth_process=constants.CREATED_NEST_B_PROCESS,
        area=created_area)


@pytest.fixture
def created_owner_beast(created_owner, created_nest):
    return Beast.objects.create(
        owner=created_owner,
        name=constants.CREATED_BEAST_NAME,
        description=constants.CREATED_BEAST_DESCRIPTION,
        experience=constants.NEW_LEVEL_EXPERIENTS,
        nest=created_nest)


@pytest.fixture
def humans_defense_get_url():
    def get_url(group_id):
        return constants.HUMANS_DEFENSE_URL.format(group_id=group_id)
    return get_url

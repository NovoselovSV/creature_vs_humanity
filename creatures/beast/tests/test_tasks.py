from copy import copy

from django.core.cache import cache
import pytest

from beast import tasks
from beast.models import Beast
from nest.models import Nest


def test_correct_obtain_resources_for_nest(
        beast_key, created_owner_beast, created_nest):
    before_nest = copy(created_nest)
    cache.set(beast_key, 'task id', 10)
    tasks.obtain_resources_for_nest.apply(
        args=(created_owner_beast.id, beast_key))
    after_nest = Nest.objects.filter(pk=created_nest.id).first()
    assert not cache.get(beast_key)
    assert after_nest
    assert (after_nest.new_creature_birth_process >
            before_nest.new_creature_birth_process)
    assert after_nest.owner == before_nest.owner
    assert after_nest.name == before_nest.name
    assert after_nest.area == before_nest.area


def test_correct_obtain_experience(
        beast_key, created_owner_beast):
    before_beast = copy(created_owner_beast)
    cache.set(beast_key, 'task id', 10)
    tasks.obtain_experience.apply(
        args=(created_owner_beast.id, beast_key))
    after_beast = Beast.objects.filter(pk=created_owner_beast.id).first()
    assert not cache.get(beast_key)
    assert after_beast
    assert after_beast.experience > before_beast.experience
    assert after_beast.owner == before_beast.owner
    assert after_beast.name == before_beast.name
    assert after_beast.description == before_beast.description
    assert after_beast.health == before_beast.health
    assert after_beast.attack == before_beast.attack
    assert after_beast.defense == before_beast.defense
    assert after_beast.nest == before_beast.nest


@pytest.mark.parametrize(
    'task', (
        tasks.obtain_experience,
        tasks.obtain_resources_for_nest
    )
)
def test_incorrect_obtain_tasks(beast_key, created_owner_beast, task):
    try:
        task.apply(args=(beast_key, created_owner_beast.id))
    except Exception:
        pytest.fail('Exception not expected')


@pytest.mark.parametrize(
    'make_diff_expect', (
        1,
    ),
    indirect=('make_diff_expect',)
)
def test_create_nest_task(
        created_owner,
        created_owner_beast,
        make_diff_expect,
        new_nest_task_data,
        created_area,
        beast_key):

    before_beast = copy(created_owner_beast)
    cache.set(beast_key, 'task id', 10)

    @make_diff_expect
    def wrapped():
        tasks.create_nest.apply(args=(
            created_owner_beast.id,
            created_owner.id,
            new_nest_task_data,
            beast_key))

    wrapped(Nest)
    new_nest = Nest.objects.filter(
        name=new_nest_task_data['name'],
        owner=created_owner.id).first()
    after_beast = Beast.objects.filter(pk=created_owner_beast.id).first()
    assert new_nest
    assert not cache.get(beast_key)

    assert new_nest.area == created_area
    assert new_nest.owner == created_owner
    assert new_nest.name == new_nest_task_data['name']

    assert after_beast.experience == before_beast.experience
    assert after_beast.owner == before_beast.owner
    assert after_beast.name == before_beast.name
    assert after_beast.description == before_beast.description
    assert after_beast.health == before_beast.health
    assert after_beast.attack == before_beast.attack
    assert after_beast.defense == before_beast.defense
    assert after_beast.nest == new_nest


@pytest.mark.parametrize(
    'make_diff_expect', (
        0,
    ),
    indirect=('make_diff_expect',)
)
@pytest.mark.parametrize(
    'incorrect_parametr_name', (
        'owner', 'beast'
    ),
)
def test_incorrect_create_nest_task(
        created_owner,
        created_owner_beast,
        make_diff_expect,
        incorrect_parametr_name,
        created_area,
        new_nest_task_data,
        beast_key):
    @make_diff_expect
    def wrapped():
        tasks.create_nest.apply(
            args=(
                0
                if incorrect_parametr_name == 'beast'
                else created_owner_beast.id,
                0
                if incorrect_parametr_name == 'owner'
                else created_owner.id,
                new_nest_task_data,
                beast_key))

    wrapped(Nest)

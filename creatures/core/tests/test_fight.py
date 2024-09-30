import random

import pytest

from beast.models import Beast
from core.fight import fight
from core.serializers import Human

SEED_FOR_BEAST_DEFEAT = 1100
SEED_FOR_BEAST_VICTORY = 1000


@pytest.mark.parametrize('make_diff_expect', (0,),
                         indirect=('make_diff_expect',))
def test_beast_win(
        created_owner_beast,
        group_members,
        created_area,
        make_diff_expect):
    before_experience = created_owner_beast.experience
    before_health = created_owner_beast.health

    @make_diff_expect
    def wrapped():
        return fight(
            created_owner_beast,
            [Human(**member) for member in group_members],
            created_area)

    response_serializer = wrapped(Beast)
    created_owner_beast.refresh_from_db()
    assert created_owner_beast.health > 0
    assert created_owner_beast.health < before_health
    assert created_owner_beast.experience > before_experience
    after_members = response_serializer.data['members']
    for member in after_members:
        assert member['health'] <= 0


@pytest.mark.parametrize('make_diff_expect', (-1,),
                         indirect=('make_diff_expect',))
def test_humans_win(
        created_owner_beast,
        strong_group_members,
        created_area,
        make_diff_expect):
    before_group = strong_group_members.copy()

    @make_diff_expect
    def wrapped():
        return fight(
            created_owner_beast,
            [Human(**member) for member in strong_group_members],
            created_area)

    response_serializer = wrapped(Beast)
    for index, member in enumerate(response_serializer.data['members']):
        before_member = before_group[index]
        assert member['health'] <= before_member['health']
        assert member['id'] == before_member['id']
        assert member['experience'] >= 0


@pytest.mark.parametrize('make_diff_expect, seed',
                         ((0, SEED_FOR_BEAST_VICTORY),
                          (-1, SEED_FOR_BEAST_DEFEAT)),
                         indirect=('make_diff_expect',))
def test_random_impact(
        created_owner_beast,
        created_area,
        seed,
        make_diff_expect):
    random.seed(seed)
    specific_group = ({'id': -2, 'health': 10, 'attack': 30},
                      {'id': -1, 'health': 10, 'attack': 30},
                      {'id': 0, 'health': 10, 'attack': 30})

    @make_diff_expect
    def wrapped():
        return fight(
            created_owner_beast,
            [Human(**member) for member in specific_group],
            created_area)

    wrapped(Beast)

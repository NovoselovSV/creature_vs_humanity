from copy import copy

import pytest
from pytest_lazy_fixtures import lf, lfc
from rest_framework import status
from rest_framework.exceptions import ValidationError

from beast.attack import request_group_attack
from beast.models import Beast
from core.exceptions import ConnectionException


@pytest.mark.parametrize(
    'attack_response, is_beast_win, make_diff_expect', (
        (lf('attack_response_data'), True, 0),
        (lf('attack_lose_response_data'), False, -1)
    ), indirect=('make_diff_expect',)
)
def test_attack_beast_normal(
        created_owner_beast,
        requests_mock,
        is_beast_win,
        make_diff_expect,
        humans_defense_get_url,
        attack_response):
    attacked_group_id = 0
    requests_mock.post(
        humans_defense_get_url(attacked_group_id),
        status_code=status.HTTP_201_CREATED,
        json=attack_response)
    before_beast = copy(created_owner_beast)

    @make_diff_expect(Beast)
    def wrapped():
        request_group_attack(created_owner_beast, attacked_group_id)

    wrapped()
    after_beast = Beast.objects.filter(pk=created_owner_beast.id).first()
    assert bool(after_beast) == is_beast_win
    if is_beast_win:
        assert after_beast.experience > before_beast.experience
        assert after_beast.health <= before_beast.health


def test_attack_beast_group_404(created_owner_beast):
    attacked_group_id = 0
    with pytest.raises(ConnectionException):
        request_group_attack(created_owner_beast, attacked_group_id)


@pytest.mark.parametrize(
    'attack_response', (
        {'experience': lfc('attack_response_data.get', 'experience'),
         'health': lfc('attack_lose_response_data.get', 'health'),
         'signature': lfc('attack_response_data.get', 'signature'),
         },
        {'experience': lfc('attack_response_data.get', 'experience'),
         'health': lfc('attack_response_data.get', 'health'),
         'signature': lfc('attack_lose_response_data.get', 'signature'),
         }
    )
)
def test_attack_beast_wrong_response(
        created_owner_beast,
        requests_mock,
        attack_response,
        humans_defense_get_url):
    attacked_group_id = 0
    requests_mock.post(
        humans_defense_get_url(attacked_group_id),
        status_code=status.HTTP_201_CREATED,
        json=attack_response)
    with pytest.raises(ValidationError):
        request_group_attack(created_owner_beast, attacked_group_id)

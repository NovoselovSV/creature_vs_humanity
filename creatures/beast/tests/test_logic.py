from django.core.cache import cache
from django.urls import reverse

import pytest
from pytest_lazy_fixtures import lf, lfc
from rest_framework import status

from beast.models import Beast
from creatures import settings


@pytest.mark.parametrize(
    'url', (
        lf('url_get_stronger'),
        lf('url_get_resources_for_nest'),
    )
)
@pytest.mark.parametrize(
    'client, expected_status', (
        (lf('created_owner_client'),
            status.HTTP_200_OK),
        (lf('created_not_owner_client'),
            status.HTTP_404_NOT_FOUND),
    )
)
@pytest.mark.parametrize(
    'beast_business, is_beast_busy', (
        (lf('beast_busy'), True),
        (None, False),
    )
)
def test_start_patch_beast_task_possibility(
        url,
        created_owner_beast,
        client,
        expected_status,
        beast_business,
        is_beast_busy,
        beast_key,
        delete_redis_n_celery_key_beast):
    response = client.patch(
        url,
        content_type='application/json')
    if is_beast_busy and expected_status == status.HTTP_200_OK:
        expected_status = status.HTTP_400_BAD_REQUEST
    assert response.status_code == expected_status
    task_id = cache.get(beast_key, False)
    assert (task_id
            if response.status_code == status.HTTP_200_OK or is_beast_busy
            else not task_id)


@pytest.mark.parametrize(
    'level_up_data', (
        {'ability_name': 'attack'},
        {'ability_name': 'defense'},
        {'ability_name': 'health'}
    )
)
@pytest.mark.parametrize(
    'client, expected_status, beast', (
        (lf('created_owner_client'),
            status.HTTP_200_OK,
            lf('created_owner_beast')),
        (lf('created_not_owner_client'),
            status.HTTP_404_NOT_FOUND,
            lf('created_owner_beast')),
        (lf('created_owner_client'),
            status.HTTP_400_BAD_REQUEST,
            lf('created_owner_weak_beast')),
        (lf('created_not_owner_client'),
            status.HTTP_404_NOT_FOUND,
            lf('created_owner_weak_beast'))
    )
)
def test_level_up_possibility(
        beast,
        client,
        set_of_beasts,
        level_up_data,
        beast_key,
        expected_status,
        comparing_object_parametrs_func,
        delete_redis_n_celery_key_beast):
    url = reverse(
        'beast:beast-level-up',
        args=(beast.id,
              ))
    response = client.patch(
        url,
        content_type='application/json',
        data=level_up_data)
    assert response.status_code == expected_status
    comparing_parameters_names = {
        'owner',
        'name',
        'description',
        'experience',
        'health',
        'attack',
        'defense',
        'nest'}
    after_beast = Beast.objects.get(pk=beast.id)
    if response.status_code == status.HTTP_200_OK:
        assert (beast.experience -
                after_beast.experience == settings.NEW_LEVEL_EXPERIENTS)
        increased_parameter = level_up_data['ability_name']
        comparing_parameters_names.remove(increased_parameter)
        comparing_parameters_names.remove('experience')
        assert (
            getattr(
                after_beast,
                increased_parameter) -
            getattr(
                beast,
                increased_parameter) ==
            settings.LVL_UP_ABILITY_NAME_VALUE[increased_parameter])
    comparing_object_parametrs_func(
        beast,
        after_beast,
        comparing_parameters_names=comparing_parameters_names)


@pytest.mark.parametrize(
    'client, expected_status, enough_beasts', (
        (lf('created_owner_client'),
            status.HTTP_201_CREATED,
            lf('set_of_beasts')),
        (lf('created_not_owner_client'),
            status.HTTP_404_NOT_FOUND,
            lf('set_of_beasts')),
        (lf('created_owner_client'),
            status.HTTP_400_BAD_REQUEST,
            None),
        (lf('created_not_owner_client'),
            status.HTTP_404_NOT_FOUND,
            None)
    )
)
@pytest.mark.parametrize(
    'beast_business, is_beast_busy', (
        (lf('beast_busy'), True),
        (None, False),
    )
)
def test_create_new_nest_possibility(
        url_create_new_nest,
        created_owner_beast,
        client,
        expected_status,
        beast_business,
        is_beast_busy,
        created_area,
        enough_beasts,
        beast_key,
        delete_redis_n_celery_key_beast):
    response = client.post(
        url_create_new_nest,
        content_type='application/json',
        data={
            'name': 'Some nest name',
            'description': 'Some nest description',
            'area': created_area.id})
    if is_beast_busy and expected_status == status.HTTP_201_CREATED:
        expected_status = status.HTTP_400_BAD_REQUEST
    assert response.status_code == expected_status
    task_id = cache.get(beast_key, False)
    assert (task_id
            if response.status_code == status.HTTP_201_CREATED or is_beast_busy
            else not task_id)


@pytest.mark.parametrize(
    'beast_business, is_beast_busy', (
        (lf('beast_busy'), True),
        (None, False),
    )
)
@pytest.mark.parametrize(
    'post_data, is_post_data_correct', (
        (lf('humans_group_data'), True),
        ({'members':
            lfc('humans_group_data.get', 'members'),
            'signature': 'wrong_signature'}, False),
        ({'members':
            lfc(list, lfc(reversed, lfc('humans_group_data.get', 'members'))),
            'signature': lfc('humans_group_data.get', 'signature')}, False),
    )
)
def test_defense_action(
        url_defense,
        beast_business,
        is_beast_busy,
        post_data,
        is_post_data_correct,
        client,
        created_owner_beast):
    response = client.post(
            url_defense,
            content_type='application/json',
            data=post_data)
    correct_request = is_beast_busy and is_post_data_correct
    expected_status = (status.HTTP_201_CREATED
                       if correct_request
                       else status.HTTP_400_BAD_REQUEST)

    assert response.status_code == expected_status
    if not correct_request:
        return
    response_json = response.json()
    assert 'members' in response_json
    members = response_json['members']
    assert len(members) > 0

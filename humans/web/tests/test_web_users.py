import pytest
from fastapi import status
from pytest_lazy_fixtures import lfc
from sqlalchemy import select

from data.user import User


def test_login_availability(unauth_client, get_temporal_user, get_user_data):
    response = unauth_client.post(
        '/users/login',
        headers={'content-type': 'application/x-www-form-urlencoded'},
        data={
            'username': get_user_data.get('username'),
            'password': get_user_data.get('password')})
    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.json()


@pytest.mark.parametrize('url', ('/users/', '/users/{user_id}'))
def test_users_get_endpoints_availability(
        unauth_client, url, get_temporal_user):
    response = unauth_client.get(url.format(user_id=get_temporal_user.id))
    assert response.status_code == status.HTTP_200_OK


def test_users_get_wrong_id(
        unauth_client, get_temporal_user):
    response = unauth_client.get('/users/0')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_users_post_endpoint_availability(
        unauth_client,
        regular_user_data):
    response = unauth_client.post(
        '/users/',
        json=regular_user_data,
        headers={
            'content-type': 'application/json'})
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
@pytest.mark.parametrize('amake_diff_expect', (1,),
                         indirect=('amake_diff_expect',))
async def test_web_users_creation(
        unauth_client,
        regular_user_data,
        get_test_db,
        amake_diff_expect):
    @amake_diff_expect(User)
    def wrapped():
        response = unauth_client.post(
            '/users/',
            json=regular_user_data,
            headers={
                'content-type': 'application/json'})
        assert response.status_code == status.HTTP_201_CREATED
        return response

    response_json = (await wrapped()).json()

    assert 'id' in response_json
    assert 'email' in response_json
    assert 'username' in response_json
    assert 'password' not in response_json
    assert response_json['email'] == regular_user_data['email']
    assert response_json['username'] == regular_user_data['username']
    assert get_test_db.execute(
        select(User).where(
            User.username == regular_user_data['username'],
            User.email == regular_user_data['email']).exists())


@pytest.mark.asyncio
@pytest.mark.parametrize('amake_diff_expect', (1,),
                         indirect=('amake_diff_expect',))
@pytest.mark.parametrize(
    'similar_data', (
        {'username': lfc(
            'regular_user_data.get', 'username')},))
async def test_web_create_2_similar_users(
        unauth_client,
        regular_user_data,
        similar_data,
        get_test_db,
        amake_diff_expect):
    @amake_diff_expect(User)
    def wrapped():
        response = unauth_client.post(
            '/users/',
            json=regular_user_data,
            headers={
                'content-type': 'application/json'})
        assert response.status_code == status.HTTP_201_CREATED
        enother_user_data = {
            'username': 'Enother_user',
            'email': 'enother@mail.net',
            'password': regular_user_data['password']}
        response = unauth_client.post(
            '/users/',
            json=(enother_user_data | similar_data),
            headers={
                'content-type': 'application/json'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    await wrapped()
    assert get_test_db.execute(
        select(User).where(
            User.username == regular_user_data['username'],
            User.email == regular_user_data['email']).exists())


@pytest.mark.parametrize('url', ('/users/', '/users/{user_id}'))
def test_users_get_endpoints_content(
        unauth_client,
        url,
        check_compare_object_with_response,
        get_temporal_user):
    response = unauth_client.get(url.format(user_id=get_temporal_user.id))
    assert response.status_code == status.HTTP_200_OK
    check_compare_object_with_response(response.json(), get_temporal_user)

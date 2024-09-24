import pytest
from pytest_lazy_fixtures import lf
from rest_framework.mixins import status


@pytest.mark.parametrize('user_diff_expect', (1,),
                         indirect=('user_diff_expect',))
def test_anonymous_can_create_user(
        client, url_users, user_diff_expect):
    @user_diff_expect
    def wrapped():
        data_dict = {'email': 'some@thing.net',
                     'username': 'someone',
                     'password': 'S0meStr0ngPassw0rd'}
        response = client.post(url_users,
                               content_type='application/json',
                               data=data_dict)
        assert response.status_code == status.HTTP_201_CREATED
        response_json = response.json()
        assert 'id' in response_json
        assert 'email' in response_json
        assert 'username' in response_json
        assert 'password' not in response_json
        assert response_json['email'] == data_dict['email']
        assert response_json['username'] == data_dict['username']

    wrapped()


@pytest.mark.parametrize('user_diff_expect', (0,),
                         indirect=('user_diff_expect',))
@pytest.mark.parametrize('invalid_data',
                         (
                             {'username': lf('created_user.username')},
                             {'email': lf('created_user.email')},
                             {'email': lf('created_user.email'),
                              'username': lf('created_user.username')},
                         ),)
def test_cant_create_user_ununique(
        client, url_users, user_diff_expect, created_user, invalid_data):
    @user_diff_expect
    def wrapped():
        data_dict = {'email': invalid_data.get('email', 'some@thing.net'),
                     'username': invalid_data.get('username', 'someone'),
                     'password': 'S0meStr0ngPassw0rd'}
        response = client.post(url_users,
                               content_type='application/json',
                               data=data_dict)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_json = response.json()
        for key in invalid_data:
            assert key in response_json

    wrapped()

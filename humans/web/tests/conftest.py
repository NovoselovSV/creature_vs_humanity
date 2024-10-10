import pytest

pytest_plugins = ('pytest_general.general_fixtures',)


@pytest.fixture
def regular_user_data():
    return {
        'username': 'Some regular user',
        'email': 'some@mail.test',
        'password': 'some_password'}

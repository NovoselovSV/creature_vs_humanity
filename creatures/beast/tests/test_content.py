import pytest
from pytest_lazy_fixtures import lf


def test_beast_has_content(
        db,
        url_beast,
        created_owner_client,
        created_owner_beast):
    response = created_owner_client.get(url_beast)
    response_json = response.json()
    assert 'id' in response_json
    assert 'name' in response_json
    assert 'description' in response_json
    assert 'health' in response_json
    assert 'attack' in response_json
    assert 'defense' in response_json
    assert 'experience' in response_json
    assert 'nest' in response_json
    assert 'in_nest' in response_json


def test_beast_content(
        db,
        url_beast,
        created_owner_client,
        created_owner_beast):
    response = created_owner_client.get(url_beast)
    response_json = response.json()
    assert response_json['id'] == created_owner_beast.id
    assert response_json['name'] == created_owner_beast.name
    assert response_json['description'] == created_owner_beast.description
    assert response_json['health'] == created_owner_beast.health
    assert response_json['attack'] == created_owner_beast.attack
    assert response_json['defense'] == created_owner_beast.defense
    assert response_json['experience'] == created_owner_beast.experience
    assert response_json['nest']['id'] == created_owner_beast.nest.id
    assert response_json['in_nest'] == created_owner_beast.in_nest


def test_not_owner_see_owner_beasts(
        url_beasts,
        created_not_owner_client,
        created_owner_beast):
    response = created_not_owner_client.get(url_beasts)
    beasts = response.json()
    assert isinstance(beasts, list)
    for beast in beasts:
        assert beast['id'] != created_owner_beast.id

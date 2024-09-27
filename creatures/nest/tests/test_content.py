from nest.tests import conftest


def test_owner_nest_has_content(url_nest, created_owner_client):
    response = created_owner_client.get(url_nest)
    response_json = response.json()
    assert 'id' in response_json
    assert 'name' in response_json
    assert 'new_creature_birth_process' in response_json
    assert 'area' in response_json
    assert 'is_giving_birth' in response_json


def test_owner_nest_content(
        url_nest,
        created_owner_client,
        created_area,
        created_nest):
    response = created_owner_client.get(url_nest)
    response_json = response.json()
    assert response_json['name'] == created_nest.name
    assert (response_json['new_creature_birth_process']
            == created_nest.new_creature_birth_process)
    assert response_json['area']['id'] == created_area.id
    assert not response_json['is_giving_birth']


def test_not_owner_see_owner_nest(
        url_nests,
        created_owner_client,
        created_not_owner_client,
        created_nest,
        created_not_owner_nest):
    response = created_not_owner_client.get(url_nests)
    nests = response.json()
    assert isinstance(nests, list)
    for nest in nests:
        assert nest['id'] != created_nest.id

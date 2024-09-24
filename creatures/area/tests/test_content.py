from area.tests import conftest


def test_area_has_content(client, url_area):
    response = client.get(url_area)
    response_json = response.json()
    assert 'name' in response_json
    assert 'description' in response_json
    assert 'attacker_attack_impact' in response_json
    assert 'attacker_defense_impact' in response_json
    assert 'defender_attack_impact' in response_json
    assert 'defender_defense_impact' in response_json


def test_area_content(client, url_area):
    response = client.get(url_area)
    response_json = response.json()
    assert response_json['name'] == conftest.AREA_NAME
    assert response_json['description'] == conftest.AREA_DESCRIPTION
    assert (response_json['attacker_attack_impact']
            == conftest.AREA_ATTACKER_ATTACK_IMPACT)
    assert (response_json['attacker_defense_impact']
            == conftest.AREA_ATTACKER_DEFENSE_IMPACT)
    assert (response_json['defender_attack_impact']
            == conftest.AREA_DEFENDER_ATTACK_IMPACT)
    assert (response_json['defender_defense_impact']
            == conftest.AREA_DEFENDER_DEFENSE_IMPACT)

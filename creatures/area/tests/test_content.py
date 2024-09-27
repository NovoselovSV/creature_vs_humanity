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


def test_area_content(client, url_area, created_area):
    response = client.get(url_area)
    response_json = response.json()
    assert response_json['name'] == created_area.name
    assert response_json['description'] == created_area.description
    assert (response_json['attacker_attack_impact']
            == created_area.attacker_attack_impact)
    assert (response_json['attacker_defense_impact']
            == created_area.attacker_defense_impact)
    assert (response_json['defender_attack_impact']
            == created_area.defender_attack_impact)
    assert (response_json['defender_defense_impact']
            == created_area.defender_defense_impact)

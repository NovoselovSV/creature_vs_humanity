import hashlib

import pytest

import settings
from data.enemy_schemas import EnemyResponseSchema, EnemySchema
from data.group_schemas import GroupAttackSchema
from data.shortcuts import get_bytes_from_stringed


def test_validation_enemy_schema(enemy_schema):
    hashed_beast_parameters = hashlib.sha256()
    hashed_beast_parameters.update(
        get_bytes_from_stringed(
            enemy_schema.name))
    hashed_beast_parameters.update(
        get_bytes_from_stringed(
            enemy_schema.health))
    hashed_beast_parameters.update(
        get_bytes_from_stringed(
            enemy_schema.attack))
    hashed_beast_parameters.update(
        get_bytes_from_stringed(
            enemy_schema.defense))
    hashed_beast_parameters.update(
        get_bytes_from_stringed(
            settings.ENEMY_SALT))
    assert enemy_schema.signature == hashed_beast_parameters.hexdigest()


@pytest.mark.parametrize('wrong_parameter',
                         (
                             {'name': 'Wrong name'},
                             {'signature': 'wrongsignature'},
                             {'signature': None},
                             {'salt': None}
                         )
                         )
def test_wrong_validation_enemy_schema(enemy_schema, wrong_parameter):
    hashed_beast_parameters = hashlib.sha256()
    hashed_beast_parameters.update(
        get_bytes_from_stringed(
            wrong_parameter.get('name', enemy_schema.name)))
    hashed_beast_parameters.update(
        get_bytes_from_stringed(
            wrong_parameter.get('health', enemy_schema.health)))
    hashed_beast_parameters.update(
        get_bytes_from_stringed(
            wrong_parameter.get('attack', enemy_schema.attack)))
    hashed_beast_parameters.update(
        get_bytes_from_stringed(
            wrong_parameter.get('defense', enemy_schema.defense)))
    hashed_beast_parameters.update(
        get_bytes_from_stringed(
            wrong_parameter.get('salt', settings.ENEMY_SALT)))
    enemy_schema_data = enemy_schema.dict()
    enemy_schema_data['signature'] = wrong_parameter.get(
        'signature', hashed_beast_parameters.hexdigest())
    with pytest.raises(ValueError):
        EnemySchema(**enemy_schema_data)


def test_enemy_response_has_signature(enemy_response_schema_data):
    assert hasattr(
        EnemyResponseSchema(
            **enemy_response_schema_data),
        'signature')


def test_group_attack_has_signature(group_schema_data):
    assert hasattr(
        GroupAttackSchema(
            **group_schema_data),
        'signature')

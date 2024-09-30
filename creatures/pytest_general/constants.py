from creatures import settings

AREA_NAME = 'Название зоны'
AREA_DESCRIPTION = 'Описание зоны'
AREA_ATTACKER_ATTACK_IMPACT = 1
AREA_ATTACKER_DEFENSE_IMPACT = 2
AREA_DEFENDER_ATTACK_IMPACT = 3
AREA_DEFENDER_DEFENSE_IMPACT = 4
CREATED_OWNER_EMAIL = 'owner@mail.com'
CREATED_OWNER_USERNAME = 'owner_username'
CREATED_NOT_OWNER_EMAIL = 'not_owner@mail.com'
CREATED_NOT_OWNER_USERNAME = 'not_owner_username'
CREATED_NEST_NAME = 'Nest name'
CREATED_NOT_OWNER_NEST_NAME = 'Nest name for not owner'
CREATED_NEST_B_PROCESS = settings.BIRTH_PROCESS_TO_APPEAR
CREATED_BEAST_NAME = 'New beast'
CREATED_BEAST_DESCRIPTION = 'New beast description'
NEST_AREA_NAME = 'Nest area name'
NEST_AREA_DESCRIPTION = 'Nest area description'
NEW_LEVEL_EXPERIENTS = settings.NEW_LEVEL_EXPERIENTS
HUMANS_DEFENSE_URL = f'{settings.ATTACK_URL}{settings.GROUP_ATTACK_ENDPOINT}'
MEMBERS_LIST = [{'id': -1, 'health': 10, 'attack': 1},
                {'id': 0, 'health': 10, 'attack': 1}]
STRONG_MEMBERS = [{'id': -1, 'health': 100, 'attack': 30},
                  {'id': 0, 'health': 100, 'attack': 30}]

import requests

from rest_framework import status
from rest_framework.renderers import JSONRenderer

from beast.serializers import AttackResponseSerializer, BeastAttackSerializer
from core.exceptions import ConnectionException
from creatures import settings


def request_group_attack(beast, target_id):
    attack_serializer = BeastAttackSerializer(beast)
    r = requests.post(
        f'{settings.ATTACK_URL}'
        f'{settings.GROUP_ATTACK_ENDPOINT.format(group_id=target_id)}',
        data=JSONRenderer().render(attack_serializer.data))
    if r.status_code != status.HTTP_201_CREATED:
        raise ConnectionException(r.json())
    response_serializer = AttackResponseSerializer(data=r.json())
    response_serializer.is_valid(raise_exception=True)
    beast_health = response_serializer.data.get('health', beast.health)
    if beast_health > 0:
        beast.increase_experience(
            response_serializer.data.get(
                'experience', 0))
        beast.set_health(beast_health)
    else:
        beast.delete()
    return response_serializer.data

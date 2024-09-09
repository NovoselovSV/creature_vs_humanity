from random import randint, shuffle

from beast.models import Beast
from core.serializers import (
    GroupResponseSerializer,
    HumanResponseSerializer,
    HumanSerializer)


def fight(beast, group, area):
    group_members = group.members.copy()
    possible_experients_to_group = beast.health / len(group_members)
    possible_experients_to_beast = sum(
        (unit.health for unit in group.members))
    queue = [*group_members, beast]
    shuffle(queue)
    while beast.health > 0 and len(queue) > 1:
        pawn = queue.pop()
        if isinstance(pawn, Beast):
            defender_attack(pawn, area, queue, randint(0, len(queue) - 1))
        else:
            attacker_attack(pawn, area, beast)
        if pawn.health > 0:
            queue.insert(0, pawn)
    if beast.health > 0:
        beast.increase_experience(possible_experients_to_beast)
        beast.set_health(beast.health)
    else:
        beast.delete()
    return list(map(lambda unit: setattr(
        unit, 'experience', possible_experients_to_group), group))


def attacker_attack(human, area, beast):
    beast.health -= (human.attack +
                     area.attacker_attack_impact -
                     beast.defense -
                     area.defender_defense_impact)


def defender_attack(beast, area, humans, attacked_human_number):
    human = humans[attacked_human_number]
    human.health -= (beast.attack +
                     area.defender_attack_impact -
                     area.attacker_defense_impact)
    if not human.health > 0:
        humans.pop(attacked_human_number)

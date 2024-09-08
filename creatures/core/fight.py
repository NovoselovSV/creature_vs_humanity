from random import randint, shuffle

from core.serializers import (
    GroupResponseSerializer,
    HumanResponseSerializer,
    HumanSerializer)


def fight(beast, group, area):
    group_members = group.copy()
    possible_expirients_to_group = beast.health / len(group_members)
    queue = list(*group_members, beast)
    shuffle(queue)
    while beast.health > 0 and len(queue) > 1:
        pawn = queue.pop()
        if isinstance(pawn, HumanSerializer):
            attacker_attack(pawn, area, beast)
        else:
            defender_attack(pawn, area, queue, randint(0, len(queue)))
        if pawn.health > 0:
            queue.insert(pawn, 0)
    beast.save()
    beast.increase_experience(sum(human.health for human in group_members))

    return GroupResponseSerializer(
        members=[
            HumanResponseSerializer(
                id=human.id,
                health=human.health,
                experience=possible_expirients_to_group)
            for human
            in group_members])


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

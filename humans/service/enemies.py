from random import randint, shuffle

from sqlalchemy.orm import Session
from sqlalchemy_utils.query_chain import copy

from data.enemy import EnemyResponseSchema, EnemySchema
from data.group import Group
from data.region import Region
from data.unit import Unit


def fight(db: Session, group: Group, enemy: EnemySchema, region: Region):
    group_members = group.members.copy()
    possible_expirients_to_member = enemy.health / len(group_members)
    queue = list(*group_members, enemy)
    shuffle(queue)
    while enemy.health > 0 and len(queue) > 1:
        pawn = queue.pop()
        if isinstance(pawn, EnemySchema):
            attacker_attack(pawn, region, queue, randint(0, len(queue)))
        else:
            defender_attack(pawn, region, enemy)
        if pawn.health > 0:
            queue.insert(pawn, 0)
    map(lambda unit: db.query(Unit).filter(Unit.id == unit.id).update(
        {'health': unit.health,
            'expirience': Unit.expirience +
            possible_expirients_to_member}), group_members)

    db.commit()
    return EnemyResponseSchema(
        health=enemy.health, expirience=sum(
            (unit.health for unit in group_members)))


def attacker_attack(creature, region, units, attacked_unit_number):
    unit = units[attacked_unit_number]
    unit.health -= (creature.attack +
                    region.attacker_attack_impact -
                    region.defender_defense_impact)
    if not unit.health > 0:
        units.pop(attacked_unit_number)


def defender_attack(unit, region, creature):
    creature.health -= (unit.attack +
                        region.defender_attack_impact -
                        creature.defense -
                        region.attacker_defense_impact)

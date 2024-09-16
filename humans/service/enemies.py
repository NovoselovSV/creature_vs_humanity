from random import randint, shuffle
import hashlib

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils.query_chain import copy

from data.enemy import EnemyResponseSchema, EnemySchema
from data.group import Group
from data.region import Region
from data.unit import Unit
import settings


def fight(db: AsyncSession, group: Group, enemy: EnemySchema, region: Region):
    group_members = group.members.copy()
    possible_experients_to_member = int(enemy.health / len(group_members))
    possible_experients_to_enemy = sum(
        (unit.health for unit in group.members))
    queue = [*group_members, enemy]
    shuffle(queue)
    while enemy.health > 0 and len(queue) > 1:
        pawn = queue.pop()
        if isinstance(pawn, EnemySchema):
            attacker_attack(pawn, region, queue, randint(0, len(queue) - 1))
        else:
            defender_attack(pawn, region, enemy)
        if pawn.health > 0:
            queue.insert(0, pawn)
    apply_group_results(db, group_members, possible_experients_to_member)
    return EnemyResponseSchema(
        health=enemy.health, experience=possible_experients_to_enemy)


def apply_group_results(db, units, experience):
    query = db.query(Unit)
    for unit in units:
        query_unit = query.filter(Unit.id == unit.id)
        if unit.health > 0:
            query_unit.update(
                {'health': unit.health,
                 'experience': Unit.experience +
                 experience})
        else:
            query_unit.delete()
    db.commit()


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

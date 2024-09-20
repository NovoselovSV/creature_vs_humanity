import httpx
from fastapi import HTTPException, status
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from .shortcuts import where_unit_id
from data.group import Group
from data.group_schemas import GroupAttackResponseSchema, GroupAttackSchema
from data.unit import Unit
import settings


async def request_beast_attack(
        db: AsyncSession,
        group: Group,
        target_id: int) -> GroupAttackResponseSchema:
    attack_data = GroupAttackSchema.from_orm(group)
    beast_defense_response = None
    async with httpx.AsyncClient() as client:
        beast_defense_response = await client.post(
            f'{settings.ATTACK_URL}'
            f'{settings.GROUP_ATTACK_ENDPOINT.format(beast_id=target_id)}',
            data=attack_data.json(),
            headers={'Content-Type': 'application/json'})
    if beast_defense_response.status_code != status.HTTP_201_CREATED:
        raise HTTPException(
            status_code=beast_defense_response.status_code,
            detail=beast_defense_response.json())
    try:
        response = GroupAttackResponseSchema(**beast_defense_response.json())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Signature not valid'
        )
    for member_dict in response.dict().get('members', []):
        member_health = member_dict.get('health', 0)
        member_id = member_dict.get('id', 0)
        if member_health > 0:
            await db.execute(where_unit_id(update(Unit).values(
                health=member_health,
                experience=Unit.experience + member_dict.get('experience', 0)),
                member_id))
        else:
            await db.execute(where_unit_id(delete(Unit), member_id))
    await db.commit()
    return response

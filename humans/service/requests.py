import httpx
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from data.group import Group, GroupAttackResponseSchema, GroupAttackSchema
from data.unit import Unit
import settings


def request_beast_attack(
        db: Session,
        group: Group,
        target_id: int) -> GroupAttackResponseSchema:
    attack_data = GroupAttackSchema.from_orm(group)
    r = httpx.post(
        f'{settings.ATTACK_URL}'
        f'{settings.GROUP_ATTACK_ENDPOINT.format(beast_id=target_id)}',
        data=attack_data.json(), headers={'Content-Type': 'application/json'})
    if r.status_code != status.HTTP_201_CREATED:
        raise HTTPException(
            status_code=r.status_code,
            detail=r.json())
    try:
        response = GroupAttackResponseSchema(**r.json())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Signature not valid'
        )
    for member_dict in response.dict().get('members', []):
        member_health = member_dict.get('health', 0)
        query = db.query(Unit).filter(Unit.id == member_dict.get('id', 0))
        if member_health > 0:
            query.update(
                {'health':
                    member_health,
                    'experience':
                    Unit.experience + member_dict.get('experience', 0)})
        else:
            query.delete()
    db.commit()
    return response

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import shortcuts as sc
from SQL_db.database import get_db
from data import group_schemas
from data.enemy_schemas import EnemyResponseSchema, EnemySchema
from data.user import User
from service import groups as groups_service
from service.headquarters import increase_recruitment_process
from service.login import get_current_user
from service.requests import request_beast_attack
from service.units import count_members, increase_members_experience


router = APIRouter(prefix='/groups')


@router.get('/',
            response_model=list[group_schemas.GroupReadSchema])
async def groups(
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)):
    return await groups_service.get_groups(db, current_user.id)


@router.get('/{group_id}',
            response_model=group_schemas.GroupReadSchema,
            responses=sc.get_error_openapi_response(
                {status.HTTP_404_NOT_FOUND: 'Group not found'}))
async def group(
        group_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)):
    return await sc.aget_object_or_404(
        groups_service.get_group,
        db,
        current_user.id,
        group_id)


@router.post('/',
             response_model=group_schemas.GroupReadShortSchema,
             status_code=status.HTTP_201_CREATED,
             responses=sc.get_error_openapi_response(
                 {status.HTTP_400_BAD_REQUEST:
                  'Name is already obtained'}))
async def group_creation(
        group_data: group_schemas.GroupWriteSchema,
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)):
    if await groups_service.get_group_by_name(db,
                                              current_user.id,
                                              group_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You have already obtaine this name')
    return await groups_service.create_group(db, current_user.id, group_data)


@router.post('/{group_id}/_defense',
             status_code=status.HTTP_201_CREATED,
             response_model=EnemyResponseSchema,
             responses=sc.get_error_openapi_response(
                 {status.HTTP_404_NOT_FOUND:
                  'Group not found',
                  status.HTTP_403_FORBIDDEN:
                  'Signature error',
                  status.HTTP_406_NOT_ACCEPTABLE:
                  'Group on hq'}))
async def group_defense(
        group_id: int,
        creature_data: EnemySchema,
        db: AsyncSession = Depends(get_db)):
    await sc.aget_object_or_404(
        groups_service.get_bare_group,
        db,
        group_id)
    if not sc.get_redis_group_key(group_id):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Group at hq')
    return await groups_service.get_ambushed(db, group_id, creature_data)


@router.post('/{group_id}/attack',
             status_code=status.HTTP_201_CREATED,
             response_model=group_schemas.GroupAttackResponseSchema,
             responses=sc.get_error_openapi_response(
                 {status.HTTP_404_NOT_FOUND: 'Group not found'}))
async def attack(
        group_id: int,
        target: group_schemas.GroupTargetSchema,
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)):
    group = await sc.aget_object_or_404(
        groups_service.get_group,
        db,
        current_user.id,
        group_id)
    sc.check_group_availability(group_id)
    return await request_beast_attack(db, group, target.target_id)


@router.patch('/{group_id}/recruite',
              responses=sc.get_error_openapi_response(
                  {status.HTTP_404_NOT_FOUND: 'Group not found',
                   status.HTTP_409_CONFLICT: 'Group is busy'}))
async def push_recruitment(
        group_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)):
    group = await sc.aget_object_or_404(
        groups_service.get_group,
        db,
        current_user.id,
        group_id)
    sc.check_group_availability(group_id)
    increase_recruitment_process(
        group.id, group.headquarter_id, await count_members(db, group.id))


@router.patch('/{group_id}/training',
              responses=sc.get_error_openapi_response(
                  {status.HTTP_404_NOT_FOUND: 'Group not found'}))
async def training(
        group_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)):
    await sc.aget_object_or_404(
        groups_service.get_group,
        db,
        current_user.id,
        group_id)
    sc.check_group_availability(group_id)
    increase_members_experience(group_id)

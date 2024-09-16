from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from data.group import GroupBuilderSchema
from service.groups import get_group_on_hq
from service.units import count_members, create_new_unit
import settings
from SQL_db.database import get_db
from data.headquarter import HeadquarterReadSchema, HeadquarterWriteSchema
from data.unit import UnitWriteSchema
from data.user import User
from service.headquarters import (
    create_new_headquarter,
    decrease_recruitment_process,
    get_headquarter,
    get_headquarter_by_name,
    get_headquarters)
from service.login import get_current_user
from web.shortcuts import (
    aget_object_or_404,
    check_group_availability,
    check_hq_availability,
    get_error_openapi_response)

router = APIRouter(prefix='/headquarters')


@router.get('/',
            response_model=list[HeadquarterReadSchema])
async def headquarters(
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)):
    return await get_headquarters(db, current_user.id)


@router.get('/{headquarter_id}',
            response_model=HeadquarterReadSchema,
            responses=get_error_openapi_response(
                {status.HTTP_404_NOT_FOUND: 'Headquarter not found'}))
async def headquarter(
        headquarter_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)):
    return await aget_object_or_404(
        get_headquarter,
        db,
        current_user.id,
        headquarter_id)


@router.post('/{headquarter_id}/deploy_unit',
             status_code=status.HTTP_201_CREATED,
             responses=get_error_openapi_response(
                 {status.HTTP_409_CONFLICT:
                  'Not enough recruitment process or other problem',
                  status.HTTP_404_NOT_FOUND:
                  'Headquarter or group not found'}))
async def deploy_unit(
        headquarter_id: int,
        unit_data: UnitWriteSchema,
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)):
    hq = await aget_object_or_404(
        get_headquarter,
        db,
        current_user.id,
        headquarter_id)
    if hq.recruitment_process < settings.RECRUITMENT_PROCESS_TO_NEW_UNIT:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Not enough recruitment process')
    await aget_object_or_404(
        get_group_on_hq,
        db,
        current_user.id,
        headquarter_id,
        unit_data.group_id)
    check_hq_availability(hq.id)
    await decrease_recruitment_process(db, hq.id)
    await create_new_unit(hq.id, unit_data, current_user.id)


@router.post('/{headquarter_id}/deploy_hq',
             status_code=status.HTTP_201_CREATED,
             responses=get_error_openapi_response(
                 {status.HTTP_409_CONFLICT:
                  'Not enough recruitment process or other problem',
                  status.HTTP_404_NOT_FOUND:
                  'Headquarter or group not found',
                  status.HTTP_400_BAD_REQUEST:
                  'Headquarter name already obtained'}))
async def deploy_hq(
        headquarter_id: int,
        group_data: GroupBuilderSchema,
        hq_data: HeadquarterWriteSchema,
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)):
    hq = await aget_object_or_404(
        get_headquarter,
        db,
        current_user.id,
        headquarter_id)
    if hq.recruitment_process < settings.RECRUITMENT_PROCESS_TO_NEW_HQ:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Not enough recruitment process')
    if await get_headquarter_by_name(db, current_user.id, hq_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You have already obtaine this name')
    group = await aget_object_or_404(
        get_group_on_hq,
        db,
        current_user.id,
        headquarter_id,
        group_data.group_id)
    check_group_availability(group.id)
    if not count_members(db, group.id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Not enough group members')
    await decrease_recruitment_process(
        db, hq.id, settings.RECRUITMENT_PROCESS_TO_NEW_HQ)
    create_new_headquarter(group.id, hq_data, current_user.id)

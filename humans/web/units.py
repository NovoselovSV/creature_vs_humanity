from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from SQL_db.database import get_db
from data.unit import UnitChangeGroupSchema, UnitLevelUpSchema, UnitReadSchema
from data.user import User, UserWriteSchema
from service.groups import get_group_on_hq
from service.login import get_current_user
from service.units import change_unit_group, get_unit, get_units, level_up_unit
from web.shortcuts import aget_object_or_404, check_group_availability, get_error_openapi_response, get_object_or_404
import settings


router = APIRouter(prefix='/units')


@router.get('/',
            response_model=list[UnitReadSchema])
async def units(
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)):
    return await get_units(db, current_user.id)


@router.get('/{unit_id}',
            response_model=UnitReadSchema,
            responses=get_error_openapi_response(
                {status.HTTP_404_NOT_FOUND: 'Unit not found'}))
async def unit(
        unit_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)):
    return await aget_object_or_404(
        get_unit,
        db,
        current_user.id,
        unit_id)


@router.patch('/{unit_id}/change_group',
              responses=get_error_openapi_response(
                  {status.HTTP_404_NOT_FOUND: 'Unit or group not found'}))
async def change_group(
        unit_id: int,
        new_group: UnitChangeGroupSchema,
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)):
    unit = await aget_object_or_404(
        get_unit,
        db,
        current_user.id,
        unit_id)
    check_group_availability((await aget_object_or_404(
        get_group_on_hq,
        db,
        current_user.id,
        unit.group.headquarter_id,
        new_group.group_id)).id)
    await change_unit_group(db, unit_id, current_user.id, new_group)


@router.patch('/{unit_id}/level_up',
              responses=get_error_openapi_response(
                  {status.HTTP_404_NOT_FOUND: 'Unit not found',
                   status.HTTP_409_CONFLICT: 'Not enough experience'}))
async def level_up(
        unit_id: int,
        parametr: UnitLevelUpSchema,
        current_user: Annotated[User, Depends(get_current_user)],
        db: AsyncSession = Depends(get_db)):
    unit = await aget_object_or_404(
        get_unit,
        db,
        current_user.id,
        unit_id)
    if unit.experience < settings.EXPERIENCE_TO_LEVEL_UP:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Not enough experience')
    check_group_availability(unit.group_id)
    await level_up_unit(db, unit.id, current_user.id, parametr.parametr_name)

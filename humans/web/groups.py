from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from SQL_db.database import get_db
from data.group import GroupReadSchema, GroupWriteSchema
from data.user import User
from service.groups import create_group, get_group, get_group_by_name, get_groups
from service.headquarters import increase_recruitment_process
from service.login import get_current_user
from service.units import count_members, increase_members_expirience
from web.shortcuts import (
    check_group_availability,
    get_error_openapi_response,
    get_object_or_404)


router = APIRouter(prefix='/groups')


@router.get('/',
            response_model=list[GroupReadSchema])
def groups(
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db)):
    return get_groups(db, current_user.id)


@router.get('/{group_id}',
            response_model=GroupReadSchema,
            responses=get_error_openapi_response(
                {status.HTTP_404_NOT_FOUND: 'Group not found'}))
def group(
        group_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db)):
    return get_object_or_404(
        get_group,
        db,
        current_user.id,
        group_id)


@router.post('/',
             responses=get_error_openapi_response(
                 {status.HTTP_400_BAD_REQUEST:
                  'Name is already obtained'}))
def group_creation(
        group_data: GroupWriteSchema,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db)):
    if get_group_by_name(db, current_user.id, group_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='You have already obtaine this name')
    create_group(db, current_user.id, group_data)


@router.patch('/{group_id}/recruite',
              responses=get_error_openapi_response(
                  {status.HTTP_404_NOT_FOUND: 'Group not found',
                   status.HTTP_409_CONFLICT: 'Group is busy'}))
def push_recruitment(
        group_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db)):
    group = get_object_or_404(
        get_group,
        db,
        current_user.id,
        group_id)
    check_group_availability(group_id)
    increase_recruitment_process(
        group.id, group.headquarter_id, count_members(db, group.id))


@router.patch('/{group_id}/training',
              responses=get_error_openapi_response(
                  {status.HTTP_404_NOT_FOUND: 'Group not found'}))
def training(
        group_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db)):
    get_object_or_404(
        get_group,
        db,
        current_user.id,
        group_id)
    check_group_availability(group_id)
    increase_members_expirience(db, group_id)

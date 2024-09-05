from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from SQL_db.database import get_db
from data.group import GroupReadSchema, GroupWriteSchema
from data.user import User
from service.groups import create_group, get_group, get_group_by_name, get_groups
from service.login import get_current_user
from web.shortcuts import get_error_openapi_response, get_object_or_404


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
             response_model=GroupReadSchema,
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
    return create_group(db, current_user.id, group_data)

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from SQL_db.database import get_db
from data.unit import UnitReadSchema
from data.user import User
from service.login import get_current_user
from service.units import get_unit, get_units
from web.shortcuts import get_error_openapi_response, get_object_or_404


router = APIRouter(prefix='/units')


@router.get('/',
            response_model=list[UnitReadSchema])
def units(
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db)):
    return get_units(db, current_user.id)


@router.get('/{unit_id}',
            response_model=UnitReadSchema,
            responses=get_error_openapi_response(
                {status.HTTP_404_NOT_FOUND: 'Unit not found'}))
def unit(
        unit_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db)):
    return get_object_or_404(
        get_unit,
        db,
        current_user.id,
        unit_id)

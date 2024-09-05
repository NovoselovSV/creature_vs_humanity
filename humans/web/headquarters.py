from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from SQL_db.database import get_db
from data.headquarter import HeadquarterReadSchema
from data.user import User
from service.headquarters import get_headquarter, get_headquarters
from service.login import get_current_user
from web.shortcuts import get_error_openapi_response, get_object_or_404

router = APIRouter(prefix='/headquarters')


@router.get('/',
            response_model=list[HeadquarterReadSchema])
def headquarters(
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db)):
    return get_headquarters(db, current_user.id)


@router.get('/{headquarter_id}',
            response_model=HeadquarterReadSchema,
            responses=get_error_openapi_response(
                {status.HTTP_404_NOT_FOUND: 'Headquarter not found'}))
def headquarter(
        headquarter_id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db)):
    return get_object_or_404(
        get_headquarter,
        db,
        current_user.id,
        headquarter_id)


# @router.post('/deploy_unit',
#              response_model=UnitCreationSchema,
#              status_code=status.HTTP_201_CREATED,
#              responses=get_error_openapi_response(
#                  {status.HTTP_409_CONFLICT:
#                   'Not enough recruitment process',
#                   status.HTTP_400_BAD_REQUEST:
#                   'You already have squad with this name'}))
# def deploy_unit(
#         hq: HeadquarterWriteSchema,
#         current_user: Annotated[User, Depends(get_current_user)],
#         db: Session = Depends(get_db)):
#     if get_headquarter_by_name(db, hq.name):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail='This username already obtained')
#     return create_user(db, hq)

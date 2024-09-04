from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from SQL_db.database import get_db
from data.headquarter import HeadquarterReadSchema
from data.user import User
from service.headquarters import get_headquarters
from service.login import get_current_user

router = APIRouter(prefix='/headquarters')


@router.get('/',
            response_model=list[HeadquarterReadSchema])
def headquarters(
        current_user: Annotated[User, Depends(get_current_user)],
        db: Session = Depends(get_db)):
    return get_headquarters(db, current_user.id)


# @router.get('/{headquarter_id}',
#             response_model=HeadquarterReadSchema,
#             responses={status.HTTP_404_NOT_FOUND: {'model': ErrorMessageSchema,
#                                                    'description':
#                                                    'Item not found'}})
# def headquarter(headquarter_id: int, db: Session = Depends(get_db)):
#     return get_object_or_404(get_headquarter, db, headquarter_id)


# @router.post('/deploy_headquarter',
#              response_model=HeadquarterReadSchema,
#              status_code=status.HTTP_201_CREATED,
#              responses={status.HTTP_400_BAD_REQUEST:
#                         {'model': ErrorMessageSchema,
#                          'description': 'Username obtained'}})
# def deploy_headquarter(
#         hq: HeadquarterWriteSchema,
#         db: Session = Depends(get_db)):
#     if get_headquarter_by_name(db, hq.name):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail='This username already obtained')
#     return create_user(db, hq)

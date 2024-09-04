from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from data.general_data import ErrorMessageSchema

from .shortcuts import get_object_or_404
from SQL_db.database import get_db
from data.user import UserReadSchema, UserWriteSchema
from service.users import create_user, get_user, get_user_username, get_users

router = APIRouter(prefix='/users')


@router.get('/', response_model=list[UserReadSchema])
def users(db: Session = Depends(get_db)):
    return get_users(db)


@router.get('/{user_id}',
            response_model=UserReadSchema,
            responses={status.HTTP_404_NOT_FOUND: {'model': ErrorMessageSchema,
                                                   'description':
                                                   'Item not found'}})
def user(user_id: int, db: Session = Depends(get_db)):
    return get_object_or_404(get_user, db, user_id)


@router.post('/', response_model=UserReadSchema,
             status_code=status.HTTP_201_CREATED)
def user_creation(user: UserWriteSchema, db: Session = Depends(get_db)):
    if get_user_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This username already obtained')
    return create_user(db, user)

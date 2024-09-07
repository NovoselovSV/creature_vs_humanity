from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import jwt

from .shortcuts import get_object_or_404, validate_credential_data
from SQL_db.database import get_db
from data.general_data import ErrorMessageSchema
from data.user import UserReadSchema, UserWriteSchema
from settings import (
    ACCESS_TOKEN_EXPIRE_DAYS,
    ALGORITHM,
    SECRET_KEY)
from data.login import Token
from service.users import create_user, get_user, get_user_username, get_users

router = APIRouter(prefix='/users')


@router.post('/login',
             responses={status.HTTP_400_BAD_REQUEST:
                        {'model': ErrorMessageSchema,
                         'description': 'Invalid credential data'}})
def login(user_data: Annotated[OAuth2PasswordRequestForm,
          Depends()], db: Session = Depends(get_db)) -> Token:
    user = validate_credential_data(db, user_data.username, user_data.password)
    return Token(
        access_token=jwt.encode(
            {'id': user.id,
             'exp': datetime.now(timezone.utc) +
             timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)},
            SECRET_KEY,
            algorithm=ALGORITHM),
        token_type='bearer')


@router.get('/{user_id}',
            response_model=UserReadSchema,
            responses={status.HTTP_404_NOT_FOUND:
                       {'model': ErrorMessageSchema,
                        'description': 'Item not found'}})
def user(user_id: int, db: Session = Depends(get_db)):
    return get_object_or_404(get_user, db, user_id)


@router.get('/', response_model=list[UserReadSchema])
def users(db: Session = Depends(get_db)):
    return get_users(db)


@router.post('/',
             response_model=UserReadSchema,
             status_code=status.HTTP_201_CREATED,
             responses={status.HTTP_400_BAD_REQUEST:
                        {'model': ErrorMessageSchema,
                         'description': 'Username obtained'}})
def user_creation(user: UserWriteSchema, db: Session = Depends(get_db)):
    if get_user_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This username already obtained')
    return create_user(db, user)

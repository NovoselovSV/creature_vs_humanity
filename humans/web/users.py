from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from . import shortcuts as sc
from SQL_db.database import get_db
from data.general_data import ErrorMessageSchema
from data.login_schemas import Token
from data.user_schemas import UserReadSchema, UserWriteSchema
from service.users import create_user, get_user, get_user_username, get_users
import settings as project_settings


router = APIRouter(prefix='/users')


@router.post('/login',
             responses={status.HTTP_400_BAD_REQUEST:
                        {'model': ErrorMessageSchema,
                         'description': 'Invalid credential data'}})
async def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends(
)], db: AsyncSession = Depends(get_db)) -> Token:
    user = await sc.validate_credential_data(db,
                                             user_data.username,
                                             user_data.password)
    return Token(
        access_token=jwt.encode(
            {'id': user.id,
             'exp': datetime.now(timezone.utc) +
             timedelta(days=project_settings.ACCESS_TOKEN_EXPIRE_DAYS)},
            project_settings.SECRET_KEY,
            algorithm=project_settings.ALGORITHM),
        token_type='bearer')


@router.get('/{user_id}',
            response_model=UserReadSchema,
            responses={status.HTTP_404_NOT_FOUND:
                       {'model': ErrorMessageSchema,
                        'description': 'Item not found'}})
async def user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await sc.aget_object_or_404(get_user, db, user_id)


@router.get('/', response_model=list[UserReadSchema])
async def users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)


@router.post('/',
             response_model=UserReadSchema,
             status_code=status.HTTP_201_CREATED,
             responses=sc.get_error_openapi_response({
                 status.HTTP_400_BAD_REQUEST:
                 'Username obtained',
                 status.HTTP_500_INTERNAL_SERVER_ERROR:
                 'Possible conflict BLOB password and '
                 'fastapi debug toolbar serializer'}))
async def user_creation(
        user: UserWriteSchema,
        db: AsyncSession = Depends(get_db)):
    if await get_user_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='This username already obtained')
    return await create_user(db, user)

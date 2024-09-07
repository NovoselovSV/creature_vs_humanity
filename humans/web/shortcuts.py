from collections.abc import Callable
from typing import Any, Dict, Type

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from SQL_db.database import Base
from data.general_data import ErrorMessageSchema
from data.user import User
from redis_app import redis_instance
from service.users import get_user_username
import settings


def validate_credential_data(
        db: Session,
        username: str,
        password: str) -> User:
    user = get_user_username(db, username)
    if not user or password != user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Login data invalid')
    return user


def validate_admin(
        db: Session,
        username: str,
        password: str) -> User:
    user = get_user_username(db, username)
    if not user or password != user.password or not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Login data invalid')
    return user


def get_object_or_404(get_object_func: Callable[[
        int, Session], Type[Base]], *args: Any) -> Type[Base]:
    obj = get_object_func(*args)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not found')
    return obj


def get_error_openapi_response(
        errors: Dict[int, str]) -> Dict[int, Dict[str, Any]]:
    return {key:
            {'model': ErrorMessageSchema,
             'description': value}
            for key, value
            in errors.items()}


def get_redis_group_key(group_id: int):
    return redis_instance.get(
        settings.REDIS_GROUP_KEY.format(
            group_id=group_id))


def check_group_availability(group_id: int):
    if get_redis_group_key(group_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Group busy')


def check_hq_availability(hq_id: int):
    if redis_instance.get(settings.REDIS_HQ_KEY.format(hq_id=hq_id)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='HQ busy')

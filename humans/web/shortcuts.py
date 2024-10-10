from collections.abc import Awaitable, Callable
from typing import Any, Dict, Type

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from SQL_db.database import Base
from data.enemy_schemas import EnemySchema
from data.general_data import ErrorMessageSchema
from data.user import User
from redis_app import redis_instance
from service.users import get_user_username


async def validate_credential_data(
        db: AsyncSession,
        username: str,
        password: str) -> User:
    user = await get_user_username(db, username)
    if not user or password != user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Login data invalid')
    return user


async def validate_admin(
        db: AsyncSession,
        username: str,
        password: str) -> User:
    user = await get_user_username(db, username)
    if not user or password != user.password or not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Login data invalid')
    return user


async def aget_object_or_404(get_object_func: Callable[[
        int, AsyncSession], Awaitable[Type[Base]]], *args: Any) -> Type[Base]:
    obj = await get_object_func(*args)
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

from typing import Any
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from data.user import User
from service.users import get_user_username
from redis_app import redis_instance
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


def create_group_task(group_id: int, task: Any, *args: Any) -> None:
    create_base_task(
        settings.REDIS_GROUP_KEY.format(group_id=group_id),
        task,
        args,
        settings.REDIS_GROUP_MISSION_SECOND)


def create_hq_task(hq_id: int, task: Any, *args: Any) -> None:
    create_base_task(
        settings.REDIS_HQ_KEY.format(hq_id=hq_id),
        task,
        args,
        settings.REDIS_HQ_WORKING_SECOND)


def create_base_task(key: str, task: Any, args: tuple[Any], time_seconds: int):
    redis_instance.set(key, task.apply_async(
        args,
        {'key': key},
        countdown=time_seconds).id,
        ex=time_seconds * settings.MULT_TASK_TIME)

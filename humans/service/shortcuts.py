from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from data.user import User
from service.users import get_user_username


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

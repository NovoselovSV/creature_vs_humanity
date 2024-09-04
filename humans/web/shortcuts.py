from collections.abc import Callable
from typing import Any, Type

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from SQL_db.database import Base


def get_object_or_404(get_object_func: Callable[[
        int, Session], Type[Base]], *args: Any) -> Type[Base]:
    obj = get_object_func(*args)
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not found')
    return obj

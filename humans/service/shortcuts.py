import asyncio
from asyncio.tasks import current_task
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Query

from SQL_db.database import SQLALCHEMY_DATABASE_URL
from data.unit import Unit
import settings
from redis_app import redis_instance

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)

CelerySession = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False)

loop = asyncio.get_event_loop()


@asynccontextmanager
async def aget_db():
    scoped_factory = async_scoped_session(
        CelerySession,
        scopefunc=current_task,
    )
    try:
        async with scoped_factory() as session:
            yield session
    finally:
        await scoped_factory.remove()


def where_unit_id(query: Query, id: int) -> Query:
    return query.where(Unit.id == id)


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

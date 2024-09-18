import asyncio
from asyncio import current_task
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any, Dict

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from SQL_db.database import SQLALCHEMY_DATABASE_URL, get_db
from celery_app import celery_app
from data.group import GroupChangeHQSchema
from data.headquarter import Headquarter
from data.unit import Unit
from redis_app import redis_instance
from service.groups import change_group_dislocation
import settings


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


def deleting_key(func):
    @wraps(func)
    def wrapper(*args, key: str, **kwargs):
        func(*args, **kwargs)
        redis_instance.delete(key)
    return wrapper


def add_db_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with aget_db() as db:
            await func(db, *args, **kwargs)
    return wrapper


@add_db_session
async def get_experience_act(db, group_id):
    await db.execute(
        update(Unit).where(
            Unit.group_id == group_id).values(
            experience=Unit.experience +
            settings.EARN_EXPERIENCE))
    await db.commit()


@add_db_session
async def create_hq_act(db: AsyncSession,
                        hq_data: Dict[str, Any],
                        director_id: int,
                        group_id: int):
    db_hq = Headquarter(**hq_data, director_id=director_id)
    db.add(db_hq)
    await db.commit()
    await db.refresh(db_hq)
    await change_group_dislocation(
        db,
        director_id,
        group_id,
        GroupChangeHQSchema(headquarter_id=db_hq.id))


@add_db_session
async def create_unit_act(db: AsyncSession,
                          unit_data: Dict[str, Any],
                          director_id: int):
    db_unit = Unit(**unit_data, director_id=director_id)
    db.add(db_unit)
    await db.commit()


@add_db_session
async def increase_recruitment_act(db: AsyncSession,
                                   headquarter_id: int,
                                   amount_units: int):
    await db.execute(
        update(Headquarter).where(
            Headquarter.id == headquarter_id).values(
            recruitment_process=Headquarter.recruitment_process +
            settings.EARN_RECRUITMENT_PROCESS * amount_units))
    await db.commit()


@celery_app.task
@deleting_key
def get_experience_celery(group_id: int):
    loop.run_until_complete(get_experience_act(group_id))


@celery_app.task
@deleting_key
def create_hq_celery(hq_data: Dict[str, Any],
                     director_id: int,
                     group_id: int):
    loop.run_until_complete(create_hq_act(hq_data, director_id, group_id))


@celery_app.task
@deleting_key
def create_unit_celery(unit_data: Dict[str, Any],
                       director_id: int):
    loop.run_until_complete(create_unit_act(unit_data, director_id))


@celery_app.task
@deleting_key
def increase_recruitment_celery(headquarter_id: int,
                                amount_units: int):
    loop.run_until_complete(
        increase_recruitment_act(
            headquarter_id,
            amount_units))

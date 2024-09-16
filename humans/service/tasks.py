from functools import wraps
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from SQL_db.database import get_db
from celery_app import celery_app
from data.group import GroupChangeHQSchema
from data.headquarter import Headquarter
from data.unit import Unit
from redis_app import redis_instance
from service.groups import change_group_dislocation
import settings


def deleting_key(func):
    @wraps(func)
    def wrapper(*args, key: str, **kwargs):
        func(*args, **kwargs)
        redis_instance.delete(key)
    return wrapper


def add_db_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = next(get_db())
        func(db, *args, **kwargs)
    return wrapper


@celery_app.task
@deleting_key
@add_db_session
def get_experience_celery(db: AsyncSession, group_id: int):
    db.query(Unit).filter(Unit.group_id == group_id).update(
        {'experience': Unit.experience + settings.EARN_EXPERIENCE})
    db.commit()


@celery_app.task
@deleting_key
@add_db_session
def create_hq_celery(db: AsyncSession,
                     hq_data: Dict[str, Any],
                     director_id: int,
                     group_id: int):
    db_hq = Headquarter(**hq_data, director_id=director_id)
    db.add(db_hq)
    db.commit()
    db.refresh(db_hq)
    change_group_dislocation(
        db,
        director_id,
        group_id,
        GroupChangeHQSchema(headquarter_id=db_hq.id))


@celery_app.task
@deleting_key
@add_db_session
def create_unit_celery(db: AsyncSession,
                       unit_data: Dict[str, Any],
                       director_id: int):
    db_unit = Unit(**unit_data, director_id=director_id)
    db.add(db_unit)
    db.commit()


@celery_app.task
@deleting_key
@add_db_session
def increase_recruitment_celery(db: AsyncSession,
                                headquarter_id: int,
                                amount_units: int):
    db.query(Headquarter).filter(Headquarter.id ==
                                 headquarter_id).update(
        {'recruitment_process':
            Headquarter.recruitment_process +
            settings.EARN_RECRUITMENT_PROCESS * amount_units})
    db.commit()

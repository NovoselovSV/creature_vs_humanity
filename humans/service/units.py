from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query

from data.unit import Unit, UnitChangeGroupSchema
from data.user import UserWriteSchema
from service.shortcuts import create_group_task, create_hq_task
from service.tasks import create_unit_celery, get_experience_celery
import settings


def get_units(db: AsyncSession, user_id: int) -> Query:
    return db.query(Unit).filter(Unit.director_id == user_id)


def get_unit(
        db: AsyncSession,
        user_id: int,
        unit_id: int) -> Unit | None:
    return get_units(db, user_id).filter(
        Unit.id == unit_id).first()


def count_members(db: AsyncSession, group_id: int) -> int:
    return db.query(Unit).filter(Unit.group_id == group_id).count()


def increase_members_experience(db: AsyncSession, group_id: int) -> None:
    create_group_task(group_id, get_experience_celery, group_id)


def create_new_unit(
        hq_id: int,
        unit_data: UserWriteSchema,
        director_id: int) -> Unit:
    create_hq_task(hq_id, create_unit_celery, unit_data.dict(), director_id)


def change_unit_group(
        db: AsyncSession,
        unit_id: int,
        director_id: int,
        new_group_data: UnitChangeGroupSchema) -> None:
    get_units(db, director_id).filter(
        Unit.id == unit_id).update(
        new_group_data.dict())
    db.commit()


def decrease_unit_experience(
        db: AsyncSession,
        unit_id: int,
        director_id: int) -> None:
    get_units(db, director_id).filter(
        Unit.id == unit_id).update(
        {'experience': Unit.experience - settings.EXPERIENCE_TO_LEVEL_UP})
    db.commit()


def level_up_unit(
        db: AsyncSession,
        unit_id: int,
        director_id: int,
        parametr_name: str) -> None:
    decrease_unit_experience(db, unit_id, director_id)
    get_units(db, director_id).filter(
        Unit.id == unit_id).update(
        {parametr_name: getattr(Unit, parametr_name) +
            settings.LEVEL_UP_TABLE[parametr_name]})
    db.commit()

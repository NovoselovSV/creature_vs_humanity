from sqlalchemy.orm import Session

from data.unit import Unit, UnitChangeGroupSchema
from data.user import UserWriteSchema
from service.shortcuts import create_group_task, create_hq_task
from service.tasks import create_unit_celery, get_expirience_celery
from redis_app import redis_instance
import settings


def get_units(db: Session, user_id: int) -> list[Unit]:
    return db.query(Unit).filter(Unit.director_id == user_id)


def get_unit(
        db: Session,
        user_id: int,
        unit_id: int) -> Unit | None:
    return db.query(Unit).filter(
        Unit.director_id == user_id,
        Unit.id == unit_id).first()


def count_members(db: Session, group_id: int) -> int:
    return db.query(Unit).filter(Unit.group_id == group_id).count()


def increase_members_expirience(db: Session, group_id: int) -> None:
    create_group_task(group_id, get_expirience_celery, group_id)


def create_new_unit(
        hq_id: int,
        unit_data: UserWriteSchema,
        director_id: int) -> Unit:
    create_hq_task(hq_id, create_unit_celery, unit_data.dict(), director_id)


def change_unit_group(
        db: Session,
        unit_id: int,
        director_id: int,
        new_group_data: UnitChangeGroupSchema) -> None:
    db.query(Unit).filter(
        Unit.id == unit_id,
        Unit.director_id == director_id).update(
        new_group_data.dict())
    db.commit()


def decrease_unit_expirience(
        db: Session,
        unit_id: int,
        director_id: int) -> None:
    db.query(Unit).filter(
        Unit.id == unit_id,
        Unit.director_id == director_id).update(
        {'expirience': Unit.expirience - settings.EXPIRIENCE_TO_LEVEL_UP})
    db.commit()


def level_up_unit(
        db: Session,
        unit_id: int,
        director_id: int,
        parametr_name: str) -> None:
    decrease_unit_expirience(db, unit_id, director_id)
    db.query(Unit).filter(
        Unit.id == unit_id,
        Unit.director_id == director_id).update(
        {parametr_name: getattr(Unit, parametr_name) +
            settings.LEVEL_UP_TABLE[parametr_name]})
    db.commit()

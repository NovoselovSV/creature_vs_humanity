from sqlalchemy.orm import Query, Session, joinedload

from data.headquarter import Headquarter, HeadquarterWriteSchema
from service.shortcuts import create_group_task
from service.tasks import create_hq_celery, increase_recruitment_celery
import settings


def get_headquarters(db: Session, user_id: int) -> Query:
    return db.query(Headquarter).options(
        joinedload(
            Headquarter.region)).filter(
        Headquarter.director_id == user_id)


def get_headquarter(
        db: Session,
        user_id: int,
        headquarter_id: int) -> Headquarter | None:
    return get_headquarters(db, user_id).filter(
        Headquarter.id == headquarter_id).first()


def get_headquarter_by_name(
        db: Session,
        user_id: int,
        headquarter_name: str) -> Headquarter | None:
    return get_headquarters(db, user_id).filter(
        Headquarter.name == headquarter_name).first()


def increase_recruitment_process(
        group_id: int,
        headquarter_id: int,
        amount_units: int) -> None:
    create_group_task(
        group_id,
        increase_recruitment_celery,
        headquarter_id,
        amount_units)


def decrease_recruitment_process(
        db: Session,
        headquarter_id: int,
        amount: int = settings.RECRUITMENT_PROCESS_TO_NEW_UNIT) -> None:
    db.query(Headquarter).filter(Headquarter.id ==
                                 headquarter_id).update(
        {'recruitment_process':
            Headquarter.recruitment_process -
            amount})
    db.commit()


def create_new_headquarter(
        group_id: int,
        hq_data: HeadquarterWriteSchema,
        director_id: int) -> None:
    create_group_task(
        group_id,
        create_hq_celery,
        hq_data.dict(),
        director_id,
        group_id)

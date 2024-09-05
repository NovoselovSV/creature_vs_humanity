from sqlalchemy.orm import Session

from data.unit import Unit, UnitChangeGroupSchema
from data.user import UserWriteSchema
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
    db.query(Unit).filter(Unit.group_id == group_id).update(
        {'expirience': Unit.expirience + settings.EARN_EXPIRIENCE})
    db.commit()


def create_new_unit(
        db: Session,
        unit_data: UserWriteSchema,
        director_id: int) -> Unit:
    db_unit = Unit(**unit_data.dict(), director_id=director_id)
    db.add(db_unit)
    db.commit()
    db.refresh(db_unit)
    return db_unit


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

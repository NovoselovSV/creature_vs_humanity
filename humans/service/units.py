from sqlalchemy.orm import Session

from data.unit import Unit


def get_units(db: Session, user_id: int) -> list[Unit]:
    return db.query(Unit).filter(Unit.director_id == user_id)


def get_unit(
        db: Session,
        user_id: int,
        unit_id: int) -> list[Unit]:
    return db.query(Unit).filter(
        Unit.director_id == user_id,
        Unit.id == unit_id).first()

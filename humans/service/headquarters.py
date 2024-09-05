from sqlalchemy.orm import Session

from data.headquarter import Headquarter


def get_headquarters(db: Session, user_id: int) -> list[Headquarter]:
    return db.query(Headquarter).filter(Headquarter.director_id == user_id)


def get_headquarter(
        db: Session,
        user_id: int,
        headquarter_id: int) -> list[Headquarter]:
    return db.query(Headquarter).filter(
        Headquarter.director_id == user_id,
        Headquarter.id == headquarter_id).first()

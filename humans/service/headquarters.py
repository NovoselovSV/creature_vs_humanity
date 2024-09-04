from sqlalchemy.orm import Session

from data.headquarter import Headquarter


def get_headquarters(db: Session, user_id: int) -> list[Headquarter]:
    return db.query(Headquarter).filter(Headquarter.director_id == user_id)

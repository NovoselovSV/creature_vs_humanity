from sqlalchemy.orm import Session

from data.headquarter import Headquarter, HeadquarterWriteSchema
import settings


def get_headquarters(db: Session, user_id: int) -> list[Headquarter]:
    return db.query(Headquarter).filter(Headquarter.director_id == user_id)


def get_headquarter(
        db: Session,
        user_id: int,
        headquarter_id: int) -> Headquarter | None:
    return db.query(Headquarter).filter(
        Headquarter.director_id == user_id,
        Headquarter.id == headquarter_id).first()


def get_headquarter_by_name(
        db: Session,
        user_id: int,
        headquarter_name: str) -> Headquarter | None:
    return db.query(Headquarter).filter(
        Headquarter.director_id == user_id,
        Headquarter.name == headquarter_name).first()


def increase_recruitment_process(
        db: Session,
        headquarter_id: int,
        amount_unit: int) -> None:
    db.query(Headquarter).filter(Headquarter.id ==
                                 headquarter_id).update(
        {'recruitment_process':
            Headquarter.recruitment_process +
            settings.EARN_RECRUITMENT_PROCESS * amount_unit})
    db.commit()


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
        db: Session,
        hq_data: HeadquarterWriteSchema,
        director_id: int) -> Headquarter:
    db_hq = Headquarter(**hq_data.dict(), director_id=director_id)
    db.add(db_hq)
    db.commit()
    db.refresh(db_hq)
    return db_hq

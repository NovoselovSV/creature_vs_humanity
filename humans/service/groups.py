from sqlalchemy import func
from sqlalchemy.orm import Session

from data.group import Group, GroupChangeHQSchema, GroupWriteSchema


def get_groups(db: Session, user_id: int) -> list[Group]:
    return db.query(Group).filter(Group.director_id == user_id)


def get_group(
        db: Session,
        user_id: int,
        group_id: int) -> Group:
    return db.query(Group).filter(
        Group.director_id == user_id,
        Group.id == group_id).first()


def get_group_by_name(
        db: Session,
        user_id: int,
        group_name: str) -> Group | None:
    return db.query(Group).filter(
        Group.director_id == user_id,
        Group.name == group_name).first()


def get_group_on_hq(
        db: Session,
        user_id: int,
        headquarter_id: int,
        group_id: int) -> Group | None:
    return db.query(Group).filter(
        Group.director_id == user_id,
        Group.id == group_id,
        Group.headquarter_id == headquarter_id).first()


def create_group(
        db: Session,
        user_id: int,
        group_data: GroupWriteSchema) -> Group:
    db_group = Group(**group_data.dict(), director_id=user_id)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def change_group_dislocation(
        db: Session,
        user_id: int,
        group_id: int,
        new_group_data: GroupChangeHQSchema) -> None:
    db.query(Group).filter(
        Group.id == group_id,
        Group.director_id == user_id).update(
        new_group_data.dict())
    db.commit()

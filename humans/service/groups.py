from sqlalchemy.orm import Query, Session, joinedload

from data.enemy import EnemyResponseSchema, EnemySchema
from data.group import Group, GroupChangeHQSchema, GroupWriteSchema
from data.headquarter import Headquarter
from service.enemies import fight
from service.regions import get_random_region


def get_groups(db: Session, user_id: int) -> Query:
    return db.query(Group).options(
        joinedload(Group.members),
        joinedload(Group.headquarter).joinedload(
            Headquarter.region)).filter(
        Group.director_id == user_id)


def get_group(
        db: Session,
        user_id: int,
        group_id: int) -> Group:
    return get_groups(db, user_id).filter(Group.id == group_id).first()


def get_group_by_name(
        db: Session,
        user_id: int,
        group_name: str) -> Group | None:
    return get_groups(db, user_id).filter(Group.name == group_name).first()


def get_group_on_hq(
        db: Session,
        user_id: int,
        headquarter_id: int,
        group_id: int) -> Group | None:
    return get_groups(db, user_id).filter(
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
    get_groups(db, user_id).filter(Group.id == group_id).update(
        new_group_data.dict())
    db.commit()


def get_ambushed(
        db: Session,
        group_id: int,
        enemy: EnemySchema) -> EnemyResponseSchema:
    return fight(
        db,
        db.query(Group).get(group_id),
        enemy,
        get_random_region(db))

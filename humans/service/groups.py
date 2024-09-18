from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query, joinedload

from data.enemy import EnemyResponseSchema, EnemySchema
from data.group import Group, GroupChangeHQSchema, GroupWriteSchema
from data.headquarter import Headquarter
from service.enemies import fight
from service.regions import get_random_region


async def get_bare_group(db: AsyncSession, group_id: int) -> Group:
    result = await db.execute(select(Group).where(Group.id == group_id))
    return result.one_or_none()


def get_groups_stmt(user_id: int) -> Query:
    return select(Group).options(
        joinedload(Group.members),
        joinedload(Group.headquarter).joinedload(
            Headquarter.region)).where(
        Group.director_id == user_id)


async def get_groups(db: AsyncSession, user_id: int) -> list[Group]:
    result = await db.execute(get_groups_stmt(user_id))
    result.unique()
    return result.scalars()


async def get_group(
        db: AsyncSession,
        user_id: int,
        group_id: int) -> Group:
    result = await db.execute(get_groups_stmt(user_id).
                              where(Group.id == group_id))
    result.unique()
    return result.scalar_one_or_none()


async def get_group_by_name(
        db: AsyncSession,
        user_id: int,
        group_name: str) -> Group | None:
    result = await db.execute(get_groups_stmt(user_id).
                              where(Group.name == group_name))
    result.unique()
    return result.scalar_one_or_none()


async def get_group_on_hq(
        db: AsyncSession,
        user_id: int,
        headquarter_id: int,
        group_id: int) -> Group | None:
    result = await db.execute(get_groups_stmt(user_id).
                              where(Group.id == group_id,
                                    Group.headquarter_id == headquarter_id))
    result.unique()
    return result.scalar_one_or_none()


async def create_group(
        db: AsyncSession,
        user_id: int,
        group_data: GroupWriteSchema) -> Group:
    db_group = Group(**group_data.dict(), director_id=user_id)
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)
    return db_group


async def change_group_dislocation(
        db: AsyncSession,
        user_id: int,
        group_id: int,
        new_group_data: GroupChangeHQSchema) -> None:
    await db.execute(update(Group).options(
        joinedload(Group.members),
        joinedload(Group.headquarter).joinedload(
            Headquarter.region)).where(
        Group.director_id == user_id,
        Group.id == group_id).values(
        **new_group_data.dict()))

    await db.commit()


async def get_ambushed(
        db: AsyncSession,
        group_id: int,
        enemy: EnemySchema) -> EnemyResponseSchema:
    return await fight(
        db,
        await db.get(Group, (group_id,)),
        enemy,
        await get_random_region(db))

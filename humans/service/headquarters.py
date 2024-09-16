from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query, joinedload

from data.headquarter import Headquarter, HeadquarterWriteSchema
from service.shortcuts import create_group_task
from service.tasks import create_hq_celery, increase_recruitment_celery
import settings


def get_base_select_hq_stmt(user_id: int) -> Query:
    return (select(Headquarter).
            options(joinedload(Headquarter.region)).
            where(Headquarter.director_id == user_id))


async def get_headquarters(
        db: AsyncSession,
        user_id: int) -> list[Headquarter]:
    result = await db.execute(get_base_select_hq_stmt(user_id))
    return result.scalars()


async def get_headquarter(
        db: AsyncSession,
        user_id: int,
        headquarter_id: int) -> Headquarter | None:
    result = await db.execute(get_base_select_hq_stmt(user_id).
                              where(Headquarter.id == headquarter_id))
    return result.scalars().one()


async def get_headquarter_by_name(
        db: AsyncSession,
        user_id: int,
        headquarter_name: str) -> Headquarter | None:
    result = await db.execute(get_base_select_hq_stmt(user_id).
                              where(Headquarter.name == headquarter_name))
    return result.scalars().one()


def increase_recruitment_process(
        group_id: int,
        headquarter_id: int,
        amount_units: int) -> None:
    create_group_task(
        group_id,
        increase_recruitment_celery,
        headquarter_id,
        amount_units)


async def decrease_recruitment_process(
        db: AsyncSession,
        headquarter_id: int,
        amount: int = settings.RECRUITMENT_PROCESS_TO_NEW_UNIT) -> None:
    await db.execute(update(Headquarter).
                     where(Headquarter.id == headquarter_id).
                     values(recruitment_process=Headquarter.
                            recruitment_process - amount))
    await db.commit()


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

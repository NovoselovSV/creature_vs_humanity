from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query

from .shortcuts import create_group_task, create_hq_task
from .tasks import create_unit_celery, get_experience_celery
from data.unit import Unit
from data.unit_schemas import UnitChangeGroupSchema
from data.user_schemas import UserWriteSchema
import settings


def get_units_stmt(user_id: int) -> Query:
    return select(Unit).where(Unit.director_id == user_id)


async def get_units(db: AsyncSession, user_id: int) -> list[Unit]:
    result = await db.execute(get_units_stmt(user_id))
    return result.scalars().all()


async def get_unit(
        db: AsyncSession,
        user_id: int,
        unit_id: int) -> Unit | None:
    result = await db.execute(get_units_stmt(
        user_id).where(Unit.id == unit_id))
    return result.scalar_one_or_none()


async def count_members(db: AsyncSession, group_id: int) -> int:
    result = await db.execute(select(func.count()).
                              where(Unit.group_id == group_id).
                              select_from(Unit))
    return result.scalar()


def increase_members_experience(group_id: int) -> None:
    create_group_task(group_id, get_experience_celery, group_id)


def create_new_unit(
        hq_id: int,
        unit_data: UserWriteSchema,
        director_id: int) -> Unit:
    create_hq_task(hq_id, create_unit_celery, unit_data.dict(), director_id)


async def change_unit_group(
        db: AsyncSession,
        unit_id: int,
        director_id: int,
        new_group_data: UnitChangeGroupSchema) -> None:
    await db.execute(update(Unit).
                     where(Unit.id == unit_id,
                           Unit.director_id == director_id).
                     values(**new_group_data.dict()))
    await db.commit()


async def decrease_unit_experience(
        db: AsyncSession,
        unit_id: int,
        director_id: int) -> None:
    await db.execute(update(Unit).
                     where(Unit.id == unit_id,
                           Unit.director_id == director_id).
                     values(experience=Unit.experience -
                            settings.EXPERIENCE_TO_LEVEL_UP))
    await db.commit()


async def level_up_unit(
        db: AsyncSession,
        unit_id: int,
        director_id: int,
        parametr_name: str) -> None:
    await decrease_unit_experience(db, unit_id, director_id)
    await db.execute(update(Unit).
                     where(Unit.id == unit_id,
                           Unit.director_id == director_id).
                     values(**{parametr_name: getattr(Unit, parametr_name) +
                               settings.LEVEL_UP_TABLE[parametr_name]}))
    await db.commit()

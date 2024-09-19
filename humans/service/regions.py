from random import choice

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.region import Region


async def get_regions(db: AsyncSession) -> list[Region]:
    result = await db.execute(select(Region))
    return result.scalars().all()


async def get_region(db: AsyncSession, region_id: int) -> Region:
    return await db.get(Region, (region_id,))


async def get_random_region(db: AsyncSession) -> Region:
    return choice(await get_regions(db))

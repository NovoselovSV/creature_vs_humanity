from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.user import User, UserWriteSchema


async def get_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    return result.scalars()


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, (user_id,))


async def get_user_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().one()


async def create_user(db: AsyncSession, user: UserWriteSchema) -> User:
    db_user = User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

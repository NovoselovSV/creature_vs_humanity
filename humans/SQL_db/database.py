import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DIALECT = 'postgresql'
DRIVER = 'asyncpg'
DB_HUMANS_DB = os.getenv('DB_HUMANS_NAME', 'humans')
DB_HUMANS_USERNAME = os.getenv('DB_HUMANS_USERNAME', 'postgres')
DB_HUMANS_PASSWORD = os.getenv('DB_HUMANS_PASSWORD', 'postgres')
DB_HUMANS_HOST = os.getenv('DB_HUMANS_HOST', 'db_humans')
DB_HUMANS_PORT = os.getenv('DB_HUMANS_PORT', '5432')
SQLALCHEMY_DATABASE_URL = (
    f'{DIALECT}+{DRIVER}://'
    f'{DB_HUMANS_USERNAME}:{DB_HUMANS_PASSWORD}'
    f'@{DB_HUMANS_HOST}:{DB_HUMANS_PORT}/{DB_HUMANS_DB}')

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

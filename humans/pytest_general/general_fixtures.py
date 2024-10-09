import hashlib
from functools import wraps

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import settings
from . import constants
from data.enemy_schemas import EnemySchema
from data.shortcuts import get_bytes_from_stringed
from data.unit_schemas import UnitAttackSchema
from data.user import User
from data.user_schemas import UserWriteSchema
from main import app
from service.login import get_current_user
from service.users import create_user
from SQL_db.database import Base, get_db


SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///memory.db'
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
)
TestingSessionLocal = sessionmaker(
    class_=AsyncSession, autocommit=False, autoflush=False, bind=engine,
)

user = UserWriteSchema(
    username=constants.USER_USERNAME,
    password=constants.USER_PASSWORD,
    email=constants.USER_EMAIL,
    is_admin=False)


async def override_db() -> AsyncSession:
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def get_test_db():
    app.dependency_overrides = {}
    app.dependency_overrides[get_db] = override_db
    yield await anext(override_db())  # noqa f825


@pytest_asyncio.fixture
async def get_temporal_user(get_test_db):
    user_db = await create_user(get_test_db, user)
    app.dependency_overrides[get_current_user] = lambda: user_db
    yield user_db
    await get_test_db.execute(delete(User).where(User.id == user_db.id))
    await get_test_db.commit()


@pytest_asyncio.fixture
async def user_client(get_temporal_user):
    with TestClient(app) as client:
        yield client


@pytest.fixture
def unauth_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def get_user_data():
    return {
        'username': constants.USER_USERNAME,
        'password': constants.USER_PASSWORD,
        'email': constants.USER_EMAIL}


@pytest.fixture
def enemy_schema():
    hashed_beast_parameters = hashlib.sha256()
    hashed_beast_parameters.update(
        get_bytes_from_stringed(
            constants.ENEMY_SCHEMA_DATA.get('name')))
    hashed_beast_parameters.update(
        get_bytes_from_stringed(
            constants.ENEMY_SCHEMA_DATA.get('health')))
    hashed_beast_parameters.update(
        get_bytes_from_stringed(
            constants.ENEMY_SCHEMA_DATA.get('attack')))
    hashed_beast_parameters.update(
        get_bytes_from_stringed(
            constants.ENEMY_SCHEMA_DATA.get('defense')))
    hashed_beast_parameters.update(
        get_bytes_from_stringed(
            settings.ENEMY_SALT))
    return EnemySchema(
        signature=hashed_beast_parameters.hexdigest(),
        **constants.ENEMY_SCHEMA_DATA)


@pytest.fixture
def enemy_response_schema_data():
    return constants.ENEMY_RESPONSE_SCHEMA_DATA


@pytest.fixture
def group_schema_data():
    return {'members': [UnitAttackSchema(
        **unit_data) for unit_data in constants.GROUP_MEMBERS_SCHEMA_DATA]}


@pytest.fixture
def make_diff_expect(get_test_db, request):
    def diff_factory_to_model(db_model):
        def fabric(wrapped_function):
            @wraps(wrapped_function)
            async def wrapper(*args, **kwargs):
                count_before = (await get_test_db.execute(
                    select(func.count()).select_from(db_model))).scalar()
                returned_value = wrapped_function()
                count_after = (await get_test_db.execute(
                    select(func.count()).select_from(db_model))).scalar()
                assert (
                    count_after
                    - count_before == request.param)
                return returned_value
            return wrapper
        return fabric
    return diff_factory_to_model

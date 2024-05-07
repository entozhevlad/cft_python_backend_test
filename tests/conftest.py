from typing import Generator, Any
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient
import settings
from main import app
import os
import asyncio
from db.session import get_db
import asyncpg
from security import create_access_token
from datetime import timedelta


CLEAN_TABLES = [
    "salaries",
    "users"

]

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system("alembic upgrade heads")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


from sqlalchemy import text
from sqlalchemy import text

@pytest.fixture(scope="module", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            # Clean the salaries table first
            await session.execute(text("TRUNCATE TABLE users CASCADE;"))
            # await session.execute(text("TRUNCATE TABLE users CASCADE;"))


async def _get_test_db():
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(settings.TEST_DATABASE_URL, future=True, echo=True)

        # create session for the interaction with database
        test_async_session = sessionmaker(test_engine, expire_on_commit=False, class_=AsyncSession)
        yield test_async_session()
    finally:
        pass

@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool("".join(settings.TEST_DATABASE_URL.split("+asyncpg")))
    yield pool
    pool.close()


@pytest.fixture
async def get_user_from_database(asyncpg_pool):

    async def get_user_from_database_by_uuid(user_id: str):
        async with asyncpg_pool.acquire() as connection:
            query = """SELECT * FROM users WHERE user_id = $1;"""
            return await connection.fetchrow(query, user_id)

    return get_user_from_database_by_uuid



@pytest.fixture
async def create_user_in_database(asyncpg_pool):
    async def create_user_in_database(user_id: str, username: str, first_name: str, last_name: str, email: str, is_active: bool, hashed_password: str):
        async with asyncpg_pool.acquire() as connection:
            await connection.execute(
                """INSERT INTO users (user_id, username, first_name, last_name, email, is_active) VALUES ($1, $2, $3, $4, $5, $6, $7);""",
                user_id, username, first_name, last_name, email, is_active, hashed_password
            )
    return create_user_in_database


def create_test_auth_headers_for_user(username: str) -> dict[str, str]:
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"Authorization": f"Bearer {access_token}"}
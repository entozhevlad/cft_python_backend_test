import asyncio
from typing import AsyncGenerator
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from settings import TEST_DATABASE_URL
from main import app
from db.models import metadata
from db.session import get_db

engine_test = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False,
                                   future=True)  # Укажите future=True для поддержки асинхронного контекстного менеджера

metadata.bind = engine_test
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:  # Вызовите async_session_maker() для создания асинхронной сессии
        yield session

app.dependency_overrides[get_db] = override_get_async_session

@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)

@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

client = TestClient(app)

@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:  # Исправлено AsyncSession на AsyncClient
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

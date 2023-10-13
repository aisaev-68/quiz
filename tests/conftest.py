import asyncio
import pytest_asyncio
from httpx import AsyncClient

from app.main import app
from app.models.database import get_db


@pytest_asyncio.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_db():
    async with get_db() as db:
        yield db


@pytest_asyncio.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as client:
        yield client
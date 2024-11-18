import asyncio
import json
from datetime import datetime

import httpcore
import pytest_asyncio
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from app.config import settings
from app.database import Base, async_session_maker, engine
from app.main import create_app
from app.orders.models import Orders
from app.rate_limiter import redis_client
from app.services.models import Services
from app.specialists.models import Specialists


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_database():
    assert settings.mode.mode == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    specialists = open_mock_json("specialists")
    orders = open_mock_json("orders")
    services = open_mock_json("services")

    for order in orders:
        order["order_time"] = datetime.strptime(order["order_time"], "%Y-%m-%dT%H:%M:%S")

    for service in services:
        service["lead_time"] = datetime.strptime(service["lead_time"], "%H:%M:%S")


    async with async_session_maker() as session:
        for Model, values in [
            (Specialists, specialists),
            (Services, services),
            (Orders, orders),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


@pytest_asyncio.fixture(scope="function")
async def ac():
    fastapi_app = create_app()
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
def app() -> TestClient:
    FastAPICache.init(RedisBackend(redis_client), prefix="cache")
    app = create_app()
    return app


@pytest_asyncio.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

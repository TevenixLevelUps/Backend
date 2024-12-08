import json
import pytest
from sqlalchemy import insert
from config import settings
from database.database import Base, async_engine, async_session

import asyncio
from specialists.models_db import Specialist_cls
from orders.order_model_db import Order_cls
from services.model_service_db import Service_cls

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 
        await conn.run_sync(Base.metadata.drop_all)
        
    def open_mock_json(model: str):
        with open(f"./tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)
        
    order = open_mock_json("order")
    service = open_mock_json("service")
    specialist = open_mock_json("specialist")
    
    async with async_session() as session:
        add_order = insert(Order_cls).values(order)
        add_service = insert(Service_cls).values(service)
        add_specialist = insert(Specialist_cls).values(specialist)
        
        await session.execute(add_order)    
        await session.execute(add_service)
        await session.execute(add_specialist)
        
        await session.commit()
        
        
@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()        
        
        
        
                
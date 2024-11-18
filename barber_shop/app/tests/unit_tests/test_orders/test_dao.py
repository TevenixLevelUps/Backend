from datetime import datetime

import pytest

from app.database import async_session_maker
from app.orders.dao import OrdersDAO
from app.orders.schemas import SOrderCreate, SOrderGet
from app.services.schemas import ServiceTitle


@pytest.mark.asyncio
@pytest.mark.parametrize("customer_name,service_title,specialist_name,order_time", [
    ("Emily Davis", "Erakez", "Djon Doe", datetime(2024, 12, 12, 4, 30, 0)),
])
async def test_create_order(
    customer_name: str,
    service_title: ServiceTitle,
    specialist_name: str,
    order_time: datetime,
) -> None:
    async with async_session_maker() as session:

        new_order = SOrderCreate(
            customer_name=customer_name,
            service_title=service_title,
            specialist_name=specialist_name,
            order_time=order_time,
        )

        await OrdersDAO.create_order(session, new_order)
        order: SOrderGet = await OrdersDAO.find_one_or_none(
            session,
            customer_name=customer_name,
            order_time=order_time,
        )
        await session.commit()

    assert order

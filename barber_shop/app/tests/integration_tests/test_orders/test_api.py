import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from app.database import async_session_maker
from app.orders.dao import OrdersDAO


@pytest.mark.asyncio
async def test_get_orders(
    app: FastAPI,
    ac: AsyncClient,
) -> None:
    get_orders_url = app.url_path_for("get_orders")
    response = await ac.get(
        get_orders_url,
    )
    async with async_session_maker() as session:
        orders_count = len(await OrdersDAO.find_all(session))
        await session.commit()

    assert len(response.json()) == orders_count
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.parametrize("customer_name,service_title,specialist_name,order_time", [
    ("Yauheni", "Erakez", "Yauheni Mukhin", "2024-11-18T13:30:00"),
])
async def test_post_orders(
    customer_name: str,
    service_title: str,
    specialist_name: str,
    order_time: str,
    app: FastAPI,
    ac: AsyncClient,
) -> None:
    put_service_url = app.url_path_for("post_order")
    response = await ac.post(
        put_service_url,
        json={
            "customer_name": customer_name,
            "service_title": service_title,
            "specialist_name": specialist_name,
            "order_time": order_time,
        }
    )

    assert response.status_code == status.HTTP_201_CREATED

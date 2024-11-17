from decimal import Decimal
from time import time
from datetime import datetime
from fastapi import FastAPI, status
from pydantic import PositiveInt
import pytest
from httpx import AsyncClient

from app.database import async_session_maker
from app.services.dao import ServicesDAO
from app.services.schemas import SServiceGet


@pytest.mark.asyncio
async def test_get_services(
    app: FastAPI,
    ac: AsyncClient,
) -> None:
    get_services_url = app.url_path_for("get_services")
    response = await ac.get(
        get_services_url,
    )
    async with async_session_maker() as session:
        services_count = len(await ServicesDAO.find_all(session))
        await session.commit()

    assert len(response.json()) == services_count
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.parametrize("title,description,price,lead_time,is_service_present,excpected_services_count", [
    ("NewService", "description", 120.0, "13:30", False, 5),
    ("Erakez", "description", 10.0, "18:30", True, 4),
])
async def test_post_service(
    title: str,
    description: str,
    price: float,
    lead_time: str,
    is_service_present: bool,
    excpected_services_count: PositiveInt,
    app: FastAPI,
    ac: AsyncClient,
) -> None:
    post_service_url = app.url_path_for("post_service")
    response = await ac.post(
        post_service_url,
        json={
            "title": title,
            "description": description,
            "price": price, 
            "lead_time": lead_time,
        }
    )
    async with async_session_maker() as session:
        services_count = len(await ServicesDAO.find_all(session))
        await session.commit()


    assert excpected_services_count == services_count
    if not is_service_present:
        assert response.status_code == status.HTTP_201_CREATED
    else:
        assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio
@pytest.mark.parametrize("title,is_service_present,excpected_services_count", [
    ("NewService", False, 4),
    ("Erakez", True, 3),
])
async def test_delete_service(
    title: str,
    is_service_present: bool,
    excpected_services_count: PositiveInt,
    app: FastAPI,
    ac: AsyncClient,
) -> None:
    delete_service_url = app.url_path_for("delete_service", service_title=title)
    response = await ac.delete(
        delete_service_url,
    )
    async with async_session_maker() as session:
        services_count = len(await ServicesDAO.find_all(session))
        await session.commit()


    assert excpected_services_count == services_count
    if is_service_present:
        assert response.status_code == status.HTTP_204_NO_CONTENT
    else:
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
@pytest.mark.parametrize("title,description,price,lead_time,is_service_present", [
    ("NewService", "description1", 120.0, "13:30:00", False),
    ("Erakez", "description2", 10.0, "18:30:00", True),
])
async def test_post_service(
    title: str,
    description: str,
    price: float,
    lead_time: str,
    is_service_present: bool,
    app: FastAPI,
    ac: AsyncClient,
) -> None:
    put_service_url = app.url_path_for("put_service")
    response = await ac.put(
        put_service_url,
        json={
            "title": title,
            "description": description,
            "price": price, 
            "lead_time": lead_time,
        }
    )
    if is_service_present:
        async with async_session_maker() as session:
            service: SServiceGet = await ServicesDAO.find_service_by_title(session, title)
            await session.commit()
        
        assert response.status_code == status.HTTP_200_OK
        assert service.description == description
        assert service.price == price
        assert service.lead_time == datetime.strptime(lead_time, "%H:%M:%S").time()
    else:
        assert response.status_code == status.HTTP_404_NOT_FOUND
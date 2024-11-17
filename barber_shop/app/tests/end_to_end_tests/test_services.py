import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient
from pydantic import PositiveInt

from app.database import async_session_maker
from app.services.dao import ServicesDAO


@pytest.mark.asyncio
@pytest.mark.parametrize("title,description,price,lead_time,is_service_present,excpected_services_count", [
    ("NewService", "description", 120.0, "13:30:00", False, 5),
    ("Erakez", "description", 10.0, "18:30:00", True, 4),
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
    async with async_session_maker() as session:
        services_count_before_post = len(await ServicesDAO.find_all(session))
        await session.commit()

    get_services_url = app.url_path_for("get_services")
    response_get_before_post = await ac.get(
        get_services_url,
    )
    assert len(response_get_before_post.json()) == services_count_before_post
    assert response_get_before_post.status_code == status.HTTP_200_OK

    post_service_url = app.url_path_for("post_service")
    response_post = await ac.post(
        post_service_url,
        json={
            "title": title,
            "description": description,
            "price": price, 
            "lead_time": lead_time,
        }
    )
    async with async_session_maker() as session:
        services_count_after_post = len(await ServicesDAO.find_all(session))
        await session.commit()

    assert excpected_services_count == services_count_after_post
    if not is_service_present:
        assert response_post.status_code == status.HTTP_201_CREATED
    else:
        assert response_post.status_code == status.HTTP_409_CONFLICT

    response_get_after_post = await ac.get(
        get_services_url,
    )
    
    assert response_get_after_post.status_code == status.HTTP_200_OK
    assert len(response_get_after_post.json()) == excpected_services_count
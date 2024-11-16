from fastapi import FastAPI, status
import pytest
from httpx import AsyncClient

from app.database import async_session_maker
from app.services.dao import ServicesDAO


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
 
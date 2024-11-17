from datetime import datetime
from decimal import Decimal
from time import time

import pytest
from app.database import async_session_maker
from app.specialists.dao import SpecialistsDAO
from fastapi import FastAPI, status
from httpx import AsyncClient
from pydantic import PositiveInt


@pytest.mark.asyncio
async def test_get_specialists(
    app: FastAPI,
    ac: AsyncClient,
) -> None:
    get_specialists_url = app.url_path_for("get_specialists")
    response = await ac.get(
        get_specialists_url,
    )
    async with async_session_maker() as session:
        specialists_count = len(await SpecialistsDAO.find_all(session))
        await session.commit()

    assert len(response.json()) == specialists_count
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.parametrize("name,is_specialist_present,excpected_specialists_count", [
    ("Charlie Brown", True, 5),
    ("NewSpec", False, 6),
])
async def test_post_specialist(
    name: str,
    is_specialist_present: bool,
    excpected_specialists_count: PositiveInt,
    app: FastAPI,
    ac: AsyncClient,
) -> None:
    post_specialist_url = app.url_path_for("post_specialist")
    response = await ac.post(
        post_specialist_url,
        json={
            "name": name,
        }
    )
    async with async_session_maker() as session:
        specialists_count = len(await SpecialistsDAO.find_all(session))
        await session.commit()


    assert excpected_specialists_count == specialists_count
    if not is_specialist_present:
        assert response.status_code == status.HTTP_201_CREATED
    else:
        assert response.status_code == status.HTTP_409_CONFLICT

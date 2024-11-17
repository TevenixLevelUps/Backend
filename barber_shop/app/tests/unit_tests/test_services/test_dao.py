from datetime import time
from decimal import Decimal
from uuid import UUID

import pytest
from app.database import async_session_maker
from app.exceptions import NoSuchServiceException
from app.services.dao import ServicesDAO
from app.services.schemas import SServiceCreate, SServiceGet


@pytest.mark.asyncio
@pytest.mark.parametrize("service_id,is_service_present", [
    ("550e8400-e29b-41d4-a716-446655440000", True),
    ("550e8400-e29b-41d4-a716-446655440002", True),
    ("5d4a4d7e-8f8a-4b7d-a2a1-9edcf8ac01fa", False),
])
async def test_find_sercice_by_id(
        service_id: UUID,
        is_service_present: bool,
) -> None:
    async with async_session_maker() as session:
        service = await ServicesDAO.find_one_or_none(session, id=service_id)
        await session.commit()
    if is_service_present:
        assert service
    else:
        assert not service


@pytest.mark.asyncio
@pytest.mark.parametrize("service_title,is_service_present", [
    ("Erakez", True),
    ("WrongTitle", False),
])
async def test_delete_service(service_title: str, is_service_present: bool) -> None:
    try:
        async with async_session_maker() as session:
            await ServicesDAO.delete_service(session, service_title)

            service = await ServicesDAO.find_one_or_none(session, title=service_title)
            assert not service
            await session.commit()
    except NoSuchServiceException:
        assert not is_service_present


@pytest.mark.asyncio
@pytest.mark.parametrize("title,description,price,lead_time,is_service_present", [
    ("Erakez", "description", Decimal(15), time(3, 12, 23), True),
    ("WrongTitle", "description2", Decimal(20), time(13, 43, 23), False),
])
async def test_update_service(
        title: str,
        description: str,
        price: Decimal,
        lead_time: time,
        is_service_present: bool,
    ) -> None:
    async with async_session_maker() as session:
        try:
            new_service = SServiceCreate(
                title=title,
                description=description,
                price=price,
                lead_time=lead_time
            )
            await ServicesDAO.update_service(session, new_service)
            await session.commit()

            service: SServiceGet = await ServicesDAO.find_one_or_none(session, title=title)

            assert service
            assert service.title == title
            assert service.description == description
            assert service.price == price
            assert service.lead_time == lead_time

        except NoSuchServiceException:
            assert not is_service_present


@pytest.mark.asyncio
@pytest.mark.parametrize("service_id,new_image_id,is_service_present", [
    ("550e8400-e29b-41d4-a716-446655440000", "550e8400-e29b-41d4-a716-446655440000", True),
    ("550e8400-e29b-41d4-a716-446655440002", "550e8400-e29b-41d4-a716-446123230000", True),
    ("5d4a4d7e-8f8a-4b7d-a2a1-9edcf8ac01fa", "550e8400-e29b-41d4-a716-564564530000", False),
])
async def test_update_service_image_id(
        service_id: UUID,
        new_image_id: UUID,
        is_service_present: bool,
) -> None:
    try:
        async with async_session_maker() as session:
            await ServicesDAO.update_image_id(session, new_image_id, service_id)
            service: SServiceGet = await ServicesDAO.find_one_or_none(session, id=service_id)
            await session.commit()

        assert service
        assert str(service.image_id) == new_image_id

    except NoSuchServiceException:
        assert not is_service_present

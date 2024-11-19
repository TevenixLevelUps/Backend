from uuid import UUID

import pytest

from app.database import async_session_maker
from app.exceptions import NoSuchSpecialistException
from app.specialists.dao import SpecialistsDAO
from app.specialists.schemas import SSpecialistGet


@pytest.mark.asyncio
@pytest.mark.parametrize("specialist_name,is_specialist_present", [
    ("Yauheni Mukhin", True),
    ("WrongName", False),
])
async def test_delete_service(specialist_name: str, is_specialist_present: bool) -> None:
    try:
        async with async_session_maker() as session:
            await SpecialistsDAO.delete_specialist(session, specialist_name)

            specialist = await SpecialistsDAO.find_one_or_none(session, name=specialist_name)
            await session.commit()

            assert not specialist

    except NoSuchSpecialistException:
        assert not is_specialist_present


@pytest.mark.asyncio
@pytest.mark.parametrize("specialist_id,new_avatar_id,is_specialist_present", [
    ("660e8400-e29b-41d4-a716-446655440004", "550e8400-e29b-41d4-a716-446238490000", True),
    ("660e8400-e29b-41d4-a716-446655440002", "550e8400-e29b-41d4-a716-446123028430", True),
    ("5d4a4d7e-8f8a-4b7d-a2a1-9edcf838973a", "550e8400-e29b-41d4-a716-523048848900", False),
])
async def test_update_specialist_image_id(
        specialist_id: UUID,
        new_avatar_id: UUID,
        is_specialist_present: bool,
) -> None:
    try:
        async with async_session_maker() as session:
            await SpecialistsDAO.update_avatar_id(session, new_avatar_id, specialist_id)
            specialist: SSpecialistGet = await SpecialistsDAO.find_one_or_none(session, id=specialist_id)
            await session.commit()

        assert specialist
        assert str(specialist.avatar_id) == new_avatar_id

    except NoSuchSpecialistException:
        assert not is_specialist_present

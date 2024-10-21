from uuid import UUID

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.specialists.models import Specialists
from app.specialists.schemas import SSpecialistGet

from app.exceptions import NoSuchSpecialistException, SpecialistAlreadyExistsException


class SpecialistsDAO(BaseDAO):
    model = Specialists

    @classmethod
    async def find_specialist_by_name(
            cls,
            session: AsyncSession,
            specialist_name: str,
    ) -> SSpecialistGet:
        specialist = await cls.find_one_or_none(session, name=specialist_name)
        if not specialist:
            raise NoSuchSpecialistException
        return specialist

    @classmethod
    async def check_specialist_not_exist(
            cls,
            session: AsyncSession,
            specialist_name: str,
    ) -> None:
        specialist = await cls.find_one_or_none(session, name=specialist_name)
        if specialist:
            raise SpecialistAlreadyExistsException

    @classmethod
    async def delete_specialist(
            cls,
            session: AsyncSession,
            specialist_name: str
    ) -> None:
        from app.specialists.avatars.dao import SpecialistAvatarsDAO

        specialist = await cls.find_specialist_by_name(session, specialist_name)
        delete_specialist_stmt = (
            delete(cls.model)
            .where(cls.model.id == specialist.id)
        )
        await SpecialistAvatarsDAO.delete_specialist_avatar(session, specialist_name)
        await session.execute(delete_specialist_stmt)

    @classmethod
    async def update_avatar_id(
            cls,
            session: AsyncSession,
            avatar_id: UUID,
            specialist_id: UUID,
    ) -> None:
        update_specialist_stmt = (
            update(cls.model)
            .where(cls.model.id == specialist_id)
            .values(avatar_id=avatar_id)
        )
        await session.execute(update_specialist_stmt)
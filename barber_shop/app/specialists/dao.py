from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.specialists.models import Specialists
from app.specialists.schemas import SSpecialist

from app.exceptions import NoSuchSpecialistException


class SpecialistsDAO(BaseDAO):
    model = Specialists

    @classmethod
    async def find_specialist_by_name(
            cls,
            session: AsyncSession,
            specialist_name: str,
    ) -> SSpecialist:
        specialist = await cls.find_one_or_none(session, name=specialist_name)
        if not specialist:
            raise NoSuchSpecialistException
        return specialist

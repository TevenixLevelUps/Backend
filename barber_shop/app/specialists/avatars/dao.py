from uuid import UUID, uuid4

from fastapi import UploadFile
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.exceptions import NotImageException, NoSuchSpecialistAvatarException, \
    AvatarForThisSpecialistAlreadyExistsException
from app.services.service_images.schemas import SServiceImage
from app.specialists.avatars.models import SpecialistAvatars
from app.specialists.dao import SpecialistsDAO


class SpecialistAvatarsDAO(BaseDAO):
    model = SpecialistAvatars

    @classmethod
    async def find_avatar_by_specialist_id(
            cls,
            session: AsyncSession,
            specialist_id: UUID
    ) -> SServiceImage:
        specialist_avatar = await cls.find_one_or_none(session, specialist_id=specialist_id)
        if not specialist_avatar:
            raise NoSuchSpecialistAvatarException
        return specialist_avatar

    @classmethod
    async def check_avatar_not_exists(
            cls,
            session: AsyncSession,
            specialist_id: UUID,
    ) -> None:
        specialist_avatar = await cls.find_one_or_none(session, specialist_id=specialist_id)
        if specialist_avatar:
            raise AvatarForThisSpecialistAlreadyExistsException

    @classmethod
    async def create_specialist_avatar(
            cls,
            session: AsyncSession,
            specialist_name: str,
            avatar: UploadFile,
    ):
        if not avatar.content_type.startswith('image/'):
            raise NotImageException

        specialist = await SpecialistsDAO.find_specialist_by_name(session, specialist_name)
        await cls.check_avatar_not_exists(session, specialist.id)

        avatar_id = uuid4()
        avatar_content = await avatar.read()
        await cls.add(
            session,
            id=avatar_id,
            specialist_id=specialist.id,
            avatar=avatar_content,
        )
        await SpecialistsDAO.update_avatar_id(session, avatar_id, specialist.id)

    @classmethod
    async def delete_specialist_avatar(cls, session: AsyncSession, specialist_name: str) -> None:
        specialist = await SpecialistsDAO.find_specialist_by_name(session, specialist_name)
        delete_specialist_avatar_stmt = (
            delete(cls.model)
            .where(cls.model.id == specialist.id)
        )
        await session.execute(delete_specialist_avatar_stmt)

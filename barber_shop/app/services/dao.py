from uuid import UUID

from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.exceptions import NoSuchServiceException
from app.services.models import Services
from app.services.schemas import SServiceGet, ServiceTitle
from app.services.service_images.dao import ServiceImagesDAO


class ServicesDAO(BaseDAO):
    model = Services

    @classmethod
    async def find_service_by_title(
            cls,
            session: AsyncSession,
            service_title: str,
    ) -> SServiceGet:
        service = await cls.find_one_or_none(session, title=service_title)
        if not service:
            raise NoSuchServiceException
        return service

    @classmethod
    async def update_image_id(
            cls,
            session: AsyncSession,
            image_id: UUID,
            service_id: UUID,
    ) -> None:
        update_service_stmt = (
            update(cls.model)
            .where(cls.model.id == service_id)
            .values(image_id=image_id)
        )
        await session.execute(update_service_stmt)

    @classmethod
    async def delete_service(
            cls,
            session: AsyncSession,
            service_title: ServiceTitle
    ) -> None:
        delete_service_stmt = (
            delete(cls.model)
            .where(cls.model.title == service_title)
        )
        await ServiceImagesDAO.delete_service_image(session, service_title)
        await session.execute(delete_service_stmt)


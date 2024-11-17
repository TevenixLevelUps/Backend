from uuid import UUID

from app.dao.base import BaseDAO
from app.exceptions import (NoSuchServiceException,
                            ServiceAlreadyExistsException)
from app.services.models import Services
from app.services.schemas import ServiceTitle, SServiceCreate, SServiceGet
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession


class ServicesDAO(BaseDAO):
    model = Services

    @classmethod
    async def find_service_by_title(
            cls,
            session: AsyncSession,
            service_title: ServiceTitle,
    ) -> SServiceGet:
        service = await cls.find_one_or_none(session, title=service_title)
        if not service:
            raise NoSuchServiceException
        return service

    @classmethod
    async def check_service_not_exist(
            cls,
            session: AsyncSession,
            service_title: ServiceTitle,
    ) -> None:
        service = await cls.find_one_or_none(session, title=service_title)
        if service:
            raise ServiceAlreadyExistsException

    @classmethod
    async def update_image_id(
            cls,
            session: AsyncSession,
            image_id: UUID,
            service_id: UUID,
    ) -> None:
        service = await cls.find_one_or_none(session, id=service_id)
        if not service:
            raise NoSuchServiceException

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
        from app.services.service_images.dao import ServiceImagesDAO

        await cls.find_service_by_title(session, service_title)

        delete_service_stmt = (
            delete(cls.model)
            .where(cls.model.title == service_title)
        )
        await ServiceImagesDAO.delete_service_image(session, service_title)
        await session.execute(delete_service_stmt)

    @classmethod
    async def update_service(
            cls,
            session: AsyncSession,
            new_service: SServiceCreate,
    ) -> None:
        await cls.find_service_by_title(session, new_service.title)

        update_service_stmt = (
            update(cls.model)
            .where(cls.model.title == new_service.title)
            .values(**new_service.model_dump())
        )
        await session.execute(update_service_stmt)

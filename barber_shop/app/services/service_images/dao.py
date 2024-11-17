from uuid import UUID, uuid4

from app.dao.base import BaseDAO
from app.exceptions import (ImageForThisServiceAlreadyExistsException,
                            NoSuchServiceImageException, NotImageException)
from app.services.dao import ServicesDAO
from app.services.schemas import ServiceTitle
from app.services.service_images.models import ServiceImages
from app.services.service_images.schemas import SServiceImage
from fastapi import UploadFile
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession


class ServiceImagesDAO(BaseDAO):
    model = ServiceImages

    @classmethod
    async def find_image_by_service_id(
            cls,
            session: AsyncSession,
            service_id: UUID
    ) -> SServiceImage:
        service_image = await cls.find_one_or_none(session, service_id=service_id)
        if not service_image:
            raise NoSuchServiceImageException
        return service_image

    @classmethod
    async def check_image_not_exists(
            cls,
            session: AsyncSession,
            service_id: UUID,
    ) -> None:
        service_image = await cls.find_one_or_none(session, service_id=service_id)
        if service_image:
            raise ImageForThisServiceAlreadyExistsException

    @classmethod
    async def create_service_image(
            cls,
            session: AsyncSession,
            service_title: ServiceTitle,
            image: UploadFile,
    ):
        if not image.content_type.startswith('image/'):
            raise NotImageException

        service = await ServicesDAO.find_service_by_title(session, service_title)
        await cls.check_image_not_exists(session, service.id)

        image_id = uuid4()
        image_content = await image.read()
        await cls.add(
            session,
            id=image_id,
            service_id=service.id,
            image=image_content,
        )
        await ServicesDAO.update_image_id(session, image_id, service.id)

    @classmethod
    async def delete_service_image(cls, session: AsyncSession, service_title: ServiceTitle) -> None:
        service = await ServicesDAO.find_service_by_title(session, service_title)
        delete_service_image_stmt = (
            delete(cls.model)
            .where(cls.model.service_id == service.id)
        )
        await session.execute(delete_service_image_stmt)

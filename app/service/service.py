import base64

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.redis_dec import cache_red, invalidate_cache
from app.models.service import Service

from ..exceptions import ServiceHTTPException
from .shema import CreateService, ServiceRespon


@invalidate_cache
async def create_service(session: AsyncSession, service_data: CreateService):
    if not service_data.name or not service_data.price:  # Пример проверки данных
        raise ServiceHTTPException.invalid_service_data

    service = Service(
        name=service_data.name,
        description=service_data.description,
        price=service_data.price,
        execution_time=service_data.execution_time,
        image=service_data.image,
    )

    try:
        session.add(service)
        await session.commit()
        await session.refresh(service)
    except Exception:
        raise ServiceHTTPException.service_creation_failed

    # Кодируем изображение в Base64
    image_base64 = base64.b64encode(service.image).decode("utf-8")

    return ServiceRespon(
        id=service.id,
        name=service.name,
        description=service.description,
        price=service.price,
        execution_time=service.execution_time,
        avatar_base64=image_base64,
    )


@cache_red(ServiceRespon)
async def get_service_by_id(session: AsyncSession, service_id: int):
    result = await session.get(Service, service_id)
    if not result:
        raise ServiceHTTPException.service_not_found

    # Кодируем изображение в Base64
    image_base64 = base64.b64encode(result.image).decode("utf-8")

    return ServiceRespon(
        id=result.id,
        name=result.name,
        description=result.description,
        price=result.price,
        execution_time=result.execution_time,
        avatar_base64=image_base64,
    )


@cache_red(ServiceRespon)
async def get_all_services(session: AsyncSession):
    result = await session.execute(select(Service))
    services = result.scalars().all()

    return [
        ServiceRespon(
            id=service.id,
            name=service.name,
            description=service.description,
            price=service.price,
            execution_time=service.execution_time,
            avatar_base64=base64.b64encode(service.image).decode("utf-8"),
        )
        for service in services
    ]


@invalidate_cache
async def update_service(
    session: AsyncSession, service_id: int, service_data: CreateService
):
    service = await session.get(Service, service_id)
    if not service:
        raise ServiceHTTPException.service_not_found

    service.name = service_data.name
    service.description = service_data.description
    service.price = service_data.price
    service.execution_time = service_data.execution_time
    service.image = service_data.image

    await session.commit()
    await session.refresh(service)

    # Кодируем изображение в Base64
    image_base64 = base64.b64encode(service.image).decode("utf-8")

    return ServiceRespon(
        id=service.id,
        name=service.name,
        description=service.description,
        price=service.price,
        execution_time=service.execution_time,
        avatar_base64=image_base64,
    )


@invalidate_cache
async def delete_service(session: AsyncSession, service_id: int):
    service = await session.get(Service, service_id)
    if not service:
        raise ServiceHTTPException.service_not_found

    await session.delete(service)
    await session.commit()

from uuid import uuid4

from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import session_getter
from app.services.dao import ServicesDAO
from app.services.schemas import ErrorSchema, ServiceTitle, SServiceCreate

router = APIRouter(
    prefix="/services",
    tags=["Services"],
)


@router.post(
        "/", 
        status_code=status.HTTP_201_CREATED,
        responses={
            status.HTTP_409_CONFLICT: {'model': ErrorSchema},
        }, 
)
async def post_service(
        service: SServiceCreate,
        session: AsyncSession = Depends(session_getter),
) -> SServiceCreate:
    await ServicesDAO.check_service_not_exist(session, service.title)
    await ServicesDAO.add(
        session,
        id=uuid4(),
        **service.model_dump(),
    )
    await session.commit()
    
    return service

@router.get(
        "/{service_title}/", 
        response_model=SServiceCreate,
        responses={
            status.HTTP_404_NOT_FOUND: {'model': ErrorSchema},
        },
)
@cache(expire=settings.redis.cache_expire_seconds)
async def get_service(
        service_title: ServiceTitle,
        session: AsyncSession = Depends(session_getter),
):
    service = await ServicesDAO.find_service_by_title(session, service_title)
    return service


@router.get("/", response_model=list[SServiceCreate])
@cache(expire=settings.redis.cache_expire_seconds)
async def get_services(session: AsyncSession = Depends(session_getter)):
    services = await ServicesDAO.find_all(session)
    return services


@router.delete(
        "/{service_title}/", 
        status_code=status.HTTP_204_NO_CONTENT,
        responses={
            status.HTTP_404_NOT_FOUND: {'model': ErrorSchema},
        },
)
async def delete_service(
        service_title: ServiceTitle,
        session: AsyncSession = Depends(session_getter),
) -> None:
    await ServicesDAO.delete_service(session, service_title)
    await session.commit()


@router.put(
        "/",
        responses={
            status.HTTP_404_NOT_FOUND: {'model': ErrorSchema},
        }, 
)
async def put_service(
        new_service: SServiceCreate,
        session: AsyncSession = Depends(session_getter),
) -> SServiceCreate:
    await ServicesDAO.update_service(session, new_service)
    await session.commit()
    
    return new_service

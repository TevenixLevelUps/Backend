from uuid import uuid4

from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import session_getter
from app.specialists.dao import SpecialistsDAO
from app.specialists.schemas import ErrorSchema, SSpecialistCreate, SSpecialistGet

router = APIRouter(
    prefix="/specialists",
    tags=["Specialists"],
)


@router.get(
    "/{specialist_name}/",
    responses={
        status.HTTP_404_NOT_FOUND: {'model': ErrorSchema},
    },
)
@cache(expire=settings.redis.cache_expire_seconds)
async def get_specialist(
        specialist_name: str,
        session: AsyncSession = Depends(session_getter),
) -> SSpecialistGet:
    specialist = await SpecialistsDAO.find_specialist_by_name(session, specialist_name)
    await session.commit()
    return specialist


@router.get("/")
@cache(expire=settings.redis.cache_expire_seconds)
async def get_specialists(session: AsyncSession = Depends(session_getter)) -> list[SSpecialistGet]:
    specialists = await SpecialistsDAO.find_all(session)
    return specialists


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {'model': ErrorSchema},
    },        
)
async def post_specialist(
        specialist: SSpecialistCreate,
        session: AsyncSession = Depends(session_getter),
) -> SSpecialistCreate:
    await SpecialistsDAO.check_specialist_not_exist(session, specialist.name)
    await SpecialistsDAO.add(
        session,
        id=uuid4(),
        **specialist.model_dump(),
    )
    await session.commit()
    return specialist


@router.delete(
    "/{specialist_name}/", 
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {'model': ErrorSchema},
    },        
)
async def delete_specialist(
        specialist_name: str,
        session: AsyncSession = Depends(session_getter),
) -> None:
    await SpecialistsDAO.delete_specialist(session, specialist_name)
    await session.commit()

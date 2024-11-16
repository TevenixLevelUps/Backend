from uuid import uuid4

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from app.database import session_getter
from app.specialists.dao import SpecialistsDAO
from app.specialists.schemas import SSpecialistGet, SSpecialistCreate
from app.config import settings

router = APIRouter(
    prefix="/specialists",
    tags=["Specialists"],
)


@router.get("/{specialist_name}/")
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


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_specialist(
        specialist: SSpecialistCreate,
        session: AsyncSession = Depends(session_getter),
) -> dict[str, str]:
    await SpecialistsDAO.check_specialist_not_exist(session, specialist.name)
    await SpecialistsDAO.add(
        session,
        id=uuid4(),
        **specialist.dict(),
    )
    await session.commit()
    return {"message": "specialist added successfully"}


@router.delete("/{specialist_name}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_specialist(
        specialist_name: str,
        session: AsyncSession = Depends(session_getter),
) -> None:
    await SpecialistsDAO.delete_specialist(session, specialist_name)
    await session.commit()

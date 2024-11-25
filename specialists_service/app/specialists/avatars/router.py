from fastapi import APIRouter, Depends, File, Response, UploadFile, status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import session_getter
from app.specialists.avatars.dao import SpecialistAvatarsDAO
from app.specialists.dao import SpecialistsDAO

router = APIRouter(
    prefix="/specialist_avatars",
    tags=["Specialist Avatars"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_specialist_avatar(
        specialist_name: str,
        avatar: UploadFile = File(...),
        session: AsyncSession = Depends(session_getter),
) -> dict[str, str]:
    await SpecialistAvatarsDAO.create_specialist_avatar(session, specialist_name, avatar)
    await session.commit()
    return {"message": "avatar added successfully"}


@router.get("/")
@cache(expire=settings.redis.cache_expire_seconds)
async def get_avatar(
        specialist_name: str,
        session: AsyncSession = Depends(session_getter),
) -> Response:
    specialist = await SpecialistsDAO.find_specialist_by_name(session, specialist_name)
    specialist_avatar = await SpecialistAvatarsDAO.find_avatar_by_specialist_id(session, specialist.id)
    await session.commit()
    return Response(content=specialist_avatar.avatar, media_type="image/")

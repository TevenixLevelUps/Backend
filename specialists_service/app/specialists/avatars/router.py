from fastapi import APIRouter, Depends, File, Response, UploadFile, status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import session_getter
from app.specialists.avatars.dao import SpecialistAvatarsDAO
from app.specialists.dao import SpecialistsDAO
from app.specialists.schemas import ErrorSchema

router = APIRouter(
    prefix="/specialist_avatars",
    tags=["Specialist Avatars"],
)


@router.post(
    "/", 
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {'model': ErrorSchema},
        status.HTTP_409_CONFLICT: {'model': ErrorSchema},
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE: {'model': ErrorSchema},
    },    
)
async def post_specialist_avatar(
        specialist_name: str,
        avatar: UploadFile = File(...),
        session: AsyncSession = Depends(session_getter),
) -> None:
    await SpecialistAvatarsDAO.create_specialist_avatar(session, specialist_name, avatar)
    await session.commit()


@router.get(
    "/",
    responses={
        status.HTTP_404_NOT_FOUND: {'model': ErrorSchema},
    },         
)
@cache(expire=settings.redis.cache_expire_seconds)
async def get_avatar(
        specialist_name: str,
        session: AsyncSession = Depends(session_getter),
) -> Response:
    specialist = await SpecialistsDAO.find_specialist_by_name(session, specialist_name)
    specialist_avatar = await SpecialistAvatarsDAO.find_avatar_by_specialist_id(session, specialist.id)
    await session.commit()
    return Response(content=specialist_avatar.avatar, media_type="image/")

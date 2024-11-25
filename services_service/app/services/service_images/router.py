from fastapi import APIRouter, Depends, File, Response, UploadFile, status
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import session_getter
from app.services.dao import ServicesDAO
from app.services.schemas import ServiceTitle
from app.services.service_images.dao import ServiceImagesDAO

router = APIRouter(
    prefix="/service_images",
    tags=["Service Images"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_service_image(
        service_title: ServiceTitle,
        image: UploadFile = File(...),
        session: AsyncSession = Depends(session_getter),
) -> dict[str, str]:
    await ServiceImagesDAO.create_service_image(session, service_title, image)
    await session.commit()
    return {"message": "image added successfully"}


@router.get("/")
@cache(expire=settings.redis.cache_expire_seconds)
async def get_image(
        service_title: ServiceTitle,
        session: AsyncSession = Depends(session_getter),
) -> Response:
    service = await ServicesDAO.find_service_by_title(session, service_title)
    service_image = await ServiceImagesDAO.find_image_by_service_id(session, service.id)
    await session.commit()
    return Response(content=service_image.image, media_type="image/")

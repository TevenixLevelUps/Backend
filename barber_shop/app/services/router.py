from uuid import uuid4

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import session_getter
from app.services.dao import ServicesDAO
from app.services.schemas import SService

router = APIRouter(
    prefix="/services",
    tags=["Services"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_service(
        service: SService,
        session: AsyncSession = Depends(session_getter),
) -> dict[str, str]:
    await ServicesDAO.add(
        session,
        id=uuid4(),
        **service.dict(),
    )
    await session.commit()
    return {"message": "service added successfully"}



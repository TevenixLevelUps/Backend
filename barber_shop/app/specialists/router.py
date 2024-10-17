from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import session_getter
from app.specialists.dao import SpecialistsDAO

router = APIRouter(
    prefix="/specialists",
    tags=["Specialists"],
)


@router.get("/{specialist_name}/")
async def get_specialist(
        specialist_name: str,
        session: AsyncSession = Depends(session_getter),
):
    specialist = await SpecialistsDAO.find_specialist_by_name(session, specialist_name)
    await session.commit()
    return specialist

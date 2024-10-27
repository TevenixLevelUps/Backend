from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_helper import db_helper
from .crud import get_specialist



async def get_specialist_by_id(specialist_id: Annotated[int, Path],
                               session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    specialist = await get_specialist(session=session, specialist_id=specialist_id)
    return specialist

from dao.base import BaseDAO
from specialists.models_db import Specialist_cls
from specialists.models import Specialist
from database.database import async_session
from sqlalchemy import select
from exeptions.exeptions import SpecilistNotFound

class SpecialistDAO(BaseDAO):
    
    model = Specialist_cls
    
    @classmethod
    async def create_specialist(cls, specialist: Specialist):
        async with async_session() as session:
            new_specialist = Specialist_cls(name=specialist.name, avatar=specialist.avatar)
            session.add(new_specialist)
            await session.commit()
            await session.refresh(new_specialist)

            return new_specialist
        
    @classmethod
    async def delete_specialist(cls, specialist_id: int):
        async with async_session() as session:
            result = await session.execute(select(Specialist_cls).where(Specialist_cls.id == specialist_id))
            specialist = result.scalar_one_or_none()
            if not specialist:
                raise SpecilistNotFound  # 404 Not Found
    
        await session.delete(specialist)
        await session.commit()
        return "Специалист удален"    
from sqlalchemy import Delete, Update

from specialists.model import Specialists
from models.BaseQuery import Querymethods
from models.database import async_session


class SpecialistsQuery(Querymethods):
    model = Specialists

    @classmethod
    async def remove_specialist(cls,specialist_id):
        async with async_session() as session:
            query = Delete(Specialists).where(Specialists.id == specialist_id)
            await session.execute(query)
            await session.commit()






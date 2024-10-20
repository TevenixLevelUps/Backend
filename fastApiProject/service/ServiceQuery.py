from sqlalchemy import Delete, Update

from models.BaseQuery import Querymethods
from models.database import async_session
from service.model import Services

from specialists.model import Specialists


class ServiceQuery(Querymethods):
    model  = Services

    @classmethod
    async def remove_service(cls, service_id):
        async with async_session() as session:
            query = Delete(Services).where(Services.id == service_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_service(cls, service_id, **data):
        async with async_session() as session:
            query = Update(Services).where(Services.id == service_id).values(data).returning(Services)
            service =  await session.execute(query)
            await session.commit()
            return service.scalar()




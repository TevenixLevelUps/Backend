from dao.base import BaseDAO
from services.model_service_db import Service_cls
from services.model_service import Service
from database.database import async_session

class Service_DAO(BaseDAO):
    
    model = Service_cls
    
    @classmethod
    async def create_service(cls, service: Service):
        async with async_session() as session:
            new_service = Service_cls(
                name=service.name,
                descripton=service.descripton,
                price=service.price,
                time=service.time,
                image=service.image
            )
            session.add(new_service)
            await session.commit()
            await session.refresh(new_service)
            return new_service
    




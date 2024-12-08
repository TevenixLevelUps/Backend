from database.database import async_session
from sqlalchemy import select
from fastapi import HTTPException

class BaseDAO:
    
    model = None
    
    @classmethod
    async def get_all(cls):
        async with async_session() as session:
            query = select(cls.model)
            answer = await session.execute(query)
            result = answer.scalars().all()
            if result:
                return result
            return HTTPException(status_code=404, detail="Список пуст")
            
    @classmethod
    async def get_by_id(cls, model_id: int):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=model_id)
            answer = await session.execute(query)
            result = answer.scalar_one_or_none()
            if result:
                return result
            return HTTPException(status_code=404, detail = "Такого id нет")


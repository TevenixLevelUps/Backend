from sqlalchemy import Select,Insert
from models.database import async_session

class Querymethods:

    model = None

    @classmethod
    async def find_by_id(cls,model_id: int):
        async with async_session() as session:
            query = Select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls,**filter_by):
        async with async_session() as session:
            query = Select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls,**filter_by):
        async with async_session() as session:
            query = Select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()


    @classmethod
    async def make_record(cls,**record_data):
        async with async_session() as session:
            query = Insert(cls.model).values(**record_data)
            await session.execute(query)
            await session.commit()
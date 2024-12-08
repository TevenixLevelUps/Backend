from orders.order_model import Order
from orders.order_model_db import Order_cls
from dao.base import BaseDAO
from specialists.models_db import Specialist_cls
from services.model_service_db import Service_cls
from database.database import async_session
from sqlalchemy import select
from datetime import timedelta
from exeptions.exeptions import ChooseAnotherTimeOrSpecilist



class Order_DAO(BaseDAO):
    
    model = Order_cls
    
    @classmethod
    async def get_specialist_from_order(cls, order: Order):
        async with async_session() as session:
            specialist_query = await session.execute(select(Specialist_cls).where(Specialist_cls.id == order.specialist_id))
            specialist_result = specialist_query.scalar_one_or_none()
            return specialist_result


    @classmethod
    async def get_service_from_order(cls, order: Order):
        async with async_session() as session:
            service_query = await session.execute(select(Service_cls).where(Service_cls.id == order.service_id))
            service_result = service_query.scalar_one_or_none()
            return service_result
        
        
    @classmethod
    async def get_time_from_order(cls, order: Order):
        async with async_session() as session:
            service_time_query = await session.execute(select(Service_cls.time).where(Service_cls.id == order.service_id))
            service_time_result = service_time_query.scalar_one_or_none()    
            return service_time_result
        
        
    @classmethod
    async def create_order(cls, order: Order):
        async with async_session() as session:
            new_order = Order_cls(client_name=order.client_name, service_id=order.service_id, specialist_id=order.specialist_id, time=order.time)
            
            session.add(new_order)
            await session.commit()
            await session.refresh(new_order)
            
            return new_order    
        
        
    @classmethod
    async def examination_of_order_time(cls, order: Order, service_time_result: int):
        async with async_session() as session:
            existing_orders_query = await session.execute(select(Order_cls).where(Order_cls.specialist_id == order.specialist_id))
            existing_orders = existing_orders_query.scalars().all()
    
            for existing_order in existing_orders:
                if abs((order.time - existing_order.time).total_seconds()) < timedelta(minutes=int(service_time_result)).total_seconds():
                    raise ChooseAnotherTimeOrSpecilist
        


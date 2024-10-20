from sqlalchemy import select, Delete

from models.BaseQuery import Querymethods
from models.database import async_session
from orders.model import Orders
from service.model import Services


class OrdersQuery(Querymethods):
    model = Orders

    @classmethod
    async def get_order_time(cls,specialist_id):
        async with (async_session() as session):
            query = select((Orders.date_time + Services.time_to_complete).label('time')
                           ).join(Services, Services.id == Orders.service_id
                                  ).where(Orders.specialist_id == specialist_id
                                          ).order_by(
                Orders.date_time.desc())

            last_order = await session.execute(query)
            last_order_time = last_order.scalar()
            return last_order_time

    @classmethod
    async def remove_order(cls,order_id:int):
        async with async_session() as session:
            query = Delete(Orders).where(Orders.id == order_id)
            await session.execute(query)
            await session.commit()


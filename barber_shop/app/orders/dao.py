from datetime import datetime, time, timedelta
from uuid import uuid4, UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.exceptions import SpecialistBusyException
from app.orders.models import Orders
from app.orders.schemas import SOrderCreate
from app.services.dao import ServicesDAO
from app.specialists.dao import SpecialistsDAO


class OrdersDAO(BaseDAO):
    model = Orders

    @classmethod
    async def check_order_time(
            cls,
            session: AsyncSession,
            order_time: datetime,
            service_time: time,
            specialist_id: UUID
    ) -> None:
        new_service_duration = timedelta(
            hours=service_time.hour,
            minutes=service_time.minute,
            seconds=service_time.second
        )
        new_service_end_time = order_time + new_service_duration

        orders = await cls.find_all(session, specialist_id=specialist_id)
        for order in orders:
            service = await ServicesDAO.find_one_or_none(session, id=order.service_id)
            service_duration = timedelta(
                hours=service.lead_time.hour,
                minutes=service.lead_time.minute,
                seconds=service.lead_time.second
            )
            service_end_time = order.order_time + service_duration

            if order_time <= service_end_time and order.order_time <= new_service_end_time:
                raise SpecialistBusyException

    @classmethod
    async def create_order(
            cls,
            session: AsyncSession,
            order: SOrderCreate,
    ) -> None:
        specialist = await SpecialistsDAO.find_specialist_by_name(session, order.specialist_name)
        service = await ServicesDAO.find_service_by_title(session, order.service_title)
        await cls.add(
            session,
            id=uuid4(),
            customer_name=order.customer_name,
            specialist_id=specialist.id,
            service_id=service.id,
            order_time=order.order_time,
        )
        await cls.check_order_time(session, order.order_time, service.lead_time, specialist.id)

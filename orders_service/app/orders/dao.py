from datetime import datetime, time, timedelta
from uuid import UUID, uuid4

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.exceptions import NoSuchOrderException, SpecialistBusyException
from app.orders.models import Orders
from app.orders.schemas import SOrderCreate
from app.rabbitmq.services import ServicesRabbit
from app.rabbitmq.specialists import SpecialistsRabbit


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
            service = await ServicesRabbit.send_request_for_get_service_by_id(order.service_id)

            lead_time = datetime.strptime(service["lead_time"], "%H:%M:%S")

            service_duration = timedelta(
                hours=lead_time.hour,
                minutes=lead_time.minute,
                seconds=lead_time.second
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
        specialist = await SpecialistsRabbit.send_request_for_get_specialist_by_name(order.specialist_name)
        service = await ServicesRabbit.send_request_for_get_service_by_title(order.service_title)

        lead_time = datetime.strptime(service["lead_time"], "%H:%M:%S")

        order.order_time = order.order_time.replace(tzinfo=None, microsecond=0, second=0)
        await cls.check_order_time(session, order.order_time, lead_time, specialist.get("id"))

        await cls.add(
            session,
            id=uuid4(),
            customer_name=order.customer_name,
            specialist_id=specialist.get("id"),
            service_id=service.get("id"),
            order_time=order.order_time,
        )

    @classmethod
    async def delete_order(
            cls,
            session: AsyncSession,
            order_to_delete: SOrderCreate,
    ) -> None:
        specialist = await SpecialistsRabbit.send_request_for_get_specialist_by_name(order_to_delete.specialist_name)
        service = await ServicesRabbit.send_request_for_get_service_by_title(order_to_delete.service_title)

        order_to_delete.order_time.replace(tzinfo=None)
        order_to_delete_from_db = await cls.find_one_or_none(
            session,
            customer_name=order_to_delete.customer_name,
            service_id=service.get("id"),
            specialist_id=specialist.get("id"),
            order_time=order_to_delete.order_time,
        )
        if not order_to_delete_from_db:
            raise NoSuchOrderException

        delete_order_stmt = (
            delete(cls.model)
            .where(cls.model.id == order_to_delete_from_db.id)
        )
        await session.execute(delete_order_stmt)

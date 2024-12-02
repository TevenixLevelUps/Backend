from datetime import datetime, timedelta
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import Select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis_dec import cache_red, invalidate_cache
from app.models.orders import Orders
from app.models.service import Service
from app.models.specialist import Specialist

from ..exceptions import OrderHTTPException, UserHTTPException
from .shema import CreateOrder
from .shema import Order as pydOrder


@invalidate_cache
async def create_order(session: AsyncSession, order_in: CreateOrder):
    fix_time = await round_near_five(order_in.order_time)

    service_result = await session.execute(
        Select(Service).where(Service.name == order_in.service_name)
    )
    specialist_result = await session.execute(
        Select(Specialist).where(Specialist.last_name == order_in.specialist_name)
    )

    service = service_result.scalars().first()
    specialist = specialist_result.scalars().first()

    if not service or not specialist:
        raise OrderHTTPException.service_or_specialist_not_found

    if not await is_specialist_available(
        session=session,
        specialist_id=specialist.id,
        order_time=fix_time,
        execution_time=service.execution_time,
    ):
        raise OrderHTTPException.specialist_not_available

    order = Orders(
        client_name=order_in.client_name,
        service_id=service.id,
        specialist_id=specialist.id,
        order_time=fix_time,
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


@cache_red(pydOrder)
async def get_order(session: AsyncSession, order_id) -> Orders | None:
    return await session.get(Orders, order_id)


@cache_red(pydOrder)
async def get_all_orders(
    session: AsyncSession,
) -> List[Orders]:
    stat = Select(Orders).order_by(Orders.id)
    result = await session.execute(stat)
    orders = result.scalars().all()
    return list(orders)


@invalidate_cache
async def delete_order(session: AsyncSession, order: Orders) -> None:
    await session.delete(order)
    await session.commit()


async def round_near_five(dt: datetime):
    new_time = (dt.minute // 5) * 5
    return dt.replace(minute=new_time, second=0, microsecond=0)


async def is_specialist_available(
    session: AsyncSession, specialist_id: int, order_time: datetime, execution_time: int
) -> bool:
    try:
        end_time = order_time + timedelta(minutes=execution_time)

        result = await session.execute(
            Select(Orders).where(
                Orders.specialist_id == specialist_id,
                or_(
                    and_(Orders.order_time >= order_time, Orders.order_time < end_time),
                    and_(
                        Orders.order_time + timedelta(minutes=execution_time)
                        > order_time,
                        Orders.order_time + timedelta(minutes=execution_time)
                        <= end_time,
                    ),
                ),
            )
        )

        orders = result.scalars().all()

        return len(orders) == 0

    except:
        return False

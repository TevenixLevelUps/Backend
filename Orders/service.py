from datetime import datetime
from datetime import timedelta
from http.client import HTTPException
from typing import List

from fastapi import status
from sqlalchemy import Select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from models.orders import Orders
from .shema import CreateOrder


async def create_order(session: AsyncSession, order_in: CreateOrder):
    fix_time = round_near_five(order_in.order_time)

    is_able = await is_specialist_available(session=session, specialist_id=order_in.specialist_id, order_time=fix_time,
                                            execution_time=order_in.execution_time)

    if not is_able:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Specialist is not available at this time")

    order = Orders(**order_in.model_dump(), order_time=fix_time)
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


async def get_order(session: AsyncSession, order_id) -> Orders | None:
    return await session.get(Orders, order_id)


async def get_all_orders(session: AsyncSession) -> List[Orders]:
    stat = Select(Orders).order_by(Orders.id)
    result = await session.execute(stat)
    orders = result.scalars().all()
    return list(orders)


async def delete_order(session: AsyncSession, order: Orders) -> None:
    await session.delete(order)
    await session.commit()


async def round_near_five(dt: datetime):
    new_time = (dt.minute // 5) * 5
    return dt.replace(minute=new_time, second=0, microsecond=0)


async def is_specialist_available(
        session: AsyncSession,
        specialist_id: int,
        order_time: datetime,
        execution_time: int
) -> bool:
    end_time = order_time + timedelta(minutes=execution_time)
    result = await session.execute(
        Select(Orders).where(
            Orders.specialist_id == specialist_id,
            or_(
                and_(Orders.order_time >= order_time, Orders.order_time < end_time),
                and_(
                    Orders.order_time + timedelta(minutes=execution_time) > order_time,
                    Orders.order_time + timedelta(minutes=execution_time) <= end_time
                )
            )
        )
    )
    return result.scalars().first() is None

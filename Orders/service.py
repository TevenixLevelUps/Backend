from typing import List

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from .shema import CreateOrder
from models.orders import Orders

async def create_order(session: AsyncSession, order_in :  CreateOrder):
    order = Orders(**order_in.model_dump())
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


async def get_order(session: AsyncSession, order_id) -> Orders | None :
    return await session.get(Orders, order_id)


async def get_all_orders(session: AsyncSession) -> List[Orders]:
    stat = Select(Orders).order_by(Orders.id)
    result = await session.execute(stat)
    orders = result.scalars().all()
    return list(orders)

async def delete_order(session: AsyncSession, order :Orders)-> None :
    await session.delete(order)
    await session.commit()
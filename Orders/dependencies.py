from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status, HTTPException
from database.db_helper import db_helper
from .shema import Order
from typing import Annotated
from pathlib import Path
from .service import get_order


async def get_order_by_id(
    order_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Order:
    order = await get_order(session, order_id)

    if order is not None:
        return order
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

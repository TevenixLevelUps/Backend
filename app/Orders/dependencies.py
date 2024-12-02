from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import db_helper

from ..exceptions import OrderHTTPException
from .service import get_order
from .shema import Order


async def get_order_by_id(
    order_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Order:
    order = await get_order(session, order_id)

    if order is not None:
        return order
    else:
        raise OrderHTTPException.order_not_found

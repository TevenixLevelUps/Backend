from fastapi import APIRouter, status, Depends
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import session_getter
from app.exceptions import WrongTimeException
from app.orders.dao import OrdersDAO
from app.orders.schemas import SOrderCreate

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_order(
        order: SOrderCreate,
        session: AsyncSession = Depends(session_getter),
) -> dict[str, str]:
    try:
        await OrdersDAO.create_order(session, order)
    except DBAPIError:
        raise WrongTimeException
    await session.commit()
    return {"message": "order added successfully"}

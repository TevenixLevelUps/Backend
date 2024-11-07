from fastapi import APIRouter
from barbeshop.schemas.orders import CreateOrder
from barbeshop.dao.dao_orders import OrderDAO
from barbeshop.db.postgresql_db import engine
from barbeshop.rate_limiter import rate_limiter

order_router = APIRouter()
order_dao = OrderDAO(engine=engine)

@order_router.post("/orders/")
async def create_order(order: CreateOrder):
    if rate_limiter.compare_count("admin"):
         return order_dao.create_order(order=order)

@order_router.get("/orders/")
async def read_orders():
    if rate_limiter.compare_count("admin"):
        return order_dao.return_orders()

@order_router.get("/orders/{order_id}")
async def read_order(order_id: int):
    if rate_limiter.compare_count("admin"):
        return order_dao.return_order(order_id=order_id)


@order_router.delete("/orders/{order_id}")
async def del_order(order_id: int):
    if rate_limiter.compare_count("admin"):
        return order_dao.del_order(order_id=order_id)
from barbeshop.addition.functions import gener_id_from_list
from barbeshop.database import list_orders
from fastapi import APIRouter, HTTPException
from barbeshop.schemas.orders import Order

order_router = APIRouter()

@order_router.post("/")
async def create_order(order: Order):
    for k, some_order in list_orders.items():
        if some_order.time == order.time:
            raise HTTPException(status_code=403, detail="Forbidden.")
    id = gener_id_from_list(list_orders)
    order.id = id
    list_orders[id] = order
    return order

@order_router.get("/")
async def read_orders():
    return list_orders

@order_router.get("/{order_id}")
async def read_order(order_id: int):
    try:
        return list_orders[order_id]
    except Exception:
        raise HTTPException(status_code=400, detail="Order not found.")


@order_router.delete("/{order_id}")
async def del_order(order_id: int):
    try:
        del list_orders[order_id]
        return list_orders
    except Exception:
        raise HTTPException(status_code=400, detail="Order not found.")
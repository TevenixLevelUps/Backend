from fastapi import APIRouter
from orders.order_model import Order
from orders.orderDAO import Order_DAO
from exeptions.exeptions import SpecilistOrServiceNotFound
from fastapi_cache.decorator import cache

orders_router = APIRouter(prefix="/orders")

# Эндпоинт для получения всех заказов
@orders_router.get("")
@cache(expire=20)
async def get_orders():
    return await Order_DAO.get_all()

# Эндпоинт для создания нового заказа
@orders_router.post("")
async def create_order(order: Order):
    
    specialist_result = await Order_DAO.get_specialist_from_order(order)
    service_result = await Order_DAO.get_service_from_order(order)
    service_time_result = await Order_DAO.get_time_from_order(order)
    
    if not specialist_result or not service_result:
        raise SpecilistOrServiceNotFound
    
    # Проверка на пересечение времени
    await Order_DAO.examination_of_order_time(order, service_time_result)
    
    # Создание нового заказа
    return await Order_DAO.create_order(order)

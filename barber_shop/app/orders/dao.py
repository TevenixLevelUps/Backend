from app.dao.base import BaseDAO
from app.orders.models import Orders


class OrdersDAO(BaseDAO):
    model = Orders

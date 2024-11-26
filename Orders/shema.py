from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseOrder(BaseModel):
    client_name: str
    service_name: str
    specialist_name: str
    order_time: datetime


class CreateOrder(BaseOrder):
    pass


class Order(BaseOrder):
    id: int
    model_config = ConfigDict(from_attributes=True)

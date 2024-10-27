from pydantic import BaseModel,ConfigDict
from datetime import datetime

class BaseOrder(BaseModel):
    client_name: str
    service_id: int
    specialist_id: int
    order_time: datetime

class CreateOrder(BaseOrder):
    pass

class Order(BaseOrder):
    id: int
    model_config = ConfigDict(from_attributes=True)
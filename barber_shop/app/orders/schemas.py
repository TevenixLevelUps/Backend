from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.services.schemas import ServiceTitle


class SOrderGet(BaseModel):
    id: UUID
    customer_name: str
    service_id: UUID
    specialist_id: UUID
    order_time: datetime


class SOrderCreate(BaseModel):
    customer_name: str
    service_title: ServiceTitle
    specialist_name: str
    order_time: datetime

from datetime import time
from decimal import Decimal

from pydantic import BaseModel


class SService(BaseModel):
    title: str
    description: str
    price: Decimal
    lead_time: time

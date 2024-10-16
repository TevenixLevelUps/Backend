from datetime import time
from decimal import Decimal

from pydantic import BaseModel, Field


class SService(BaseModel):
    title: str = Field(..., max_length=255)
    description: str | None
    price: Decimal
    lead_time: time

from datetime import time
from decimal import Decimal
from typing import TypeAlias, Annotated
from uuid import UUID

from annotated_types import MaxLen
from pydantic import BaseModel

ServiceTitle: TypeAlias = Annotated[str, MaxLen(255)]


class SServiceCreate(BaseModel):
    title: ServiceTitle
    description: str | None
    price: Decimal
    lead_time: time


class SServiceGet(BaseModel):
    id: UUID
    title: ServiceTitle
    description: str | None
    price: Decimal
    lead_time: time
    image_id: UUID | None

from pydantic import BaseModel, Field
from barbeshop.addition.patterns import orders_pattern

class CreateOrder(BaseModel):
    client_name: str = Field("P Diddi")
    expert_name: str = Field("Valeri Djmishenko")
    time_start: str | None = Field("13:00", pattern=orders_pattern)
    id_service: int

class UpdateOrder(BaseModel):
    id: int | None = None
    client_name: str | None = Field("P Diddi")
    expert_name: str | None = None
    time_start: str | None = None
    time_end: str | None = None
    id_service: int | None = None

class ReadOrder(BaseModel):
    id: int | None = None
    client_name: str | None = None
    expert_name: str | None = None
    time_start: str | None = None
    time_end: str | None = None
    id_service: int | None = None

    def serializer(self):
        return vars(self)
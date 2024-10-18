from pydantic import BaseModel, Field
from barbeshop.addition.patterns import orders_pattern

class Order(BaseModel):
    id: int
    client_name: str = Field("P Diddi")
    exper_name: str
    time: str = Field("13:00", pattern=orders_pattern)
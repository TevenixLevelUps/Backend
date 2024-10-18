from pydantic import BaseModel, Field
from barbeshop.addition.patterns import services_pattern

class Service(BaseModel):
    id: int | None = None
    name: str = Field("Classic haircut")
    describe: str | None = Field("Mojno corotko ili dlino")
    price: float = Field(10.5)
    time: str = Field("01:00", pattern=services_pattern)
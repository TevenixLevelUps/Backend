from pydantic import BaseModel, Field
from barbeshop.addition.patterns import services_pattern

class CreateService(BaseModel):
    name: str = Field("Classic haircut")
    describe: str = Field("Mojno corotko ili dlino")
    price: float = Field(10.5)
    time: str = Field("01:00", pattern=services_pattern)

class UpdateService(BaseModel):
    name: str | None = Field("Classic haircut")
    describe: str | None = Field("Mojno corotko ili dlino")
    price: float | None = Field(10.5)
    time: str | None = Field("01:00", pattern=services_pattern)
    
class ReadService(BaseModel):
    id: int 
    name: str 
    describe: str 
    price: float 
    time: str

    def serializer(self):
        return vars(self)
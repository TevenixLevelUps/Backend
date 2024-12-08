from pydantic import BaseModel
from datetime import datetime

class Order(BaseModel):
    client_name: str
    service_id: int
    specialist_id: int
    time: datetime
    
    class Config:
        orm_mode = True

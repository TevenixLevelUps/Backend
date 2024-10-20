from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class Service(BaseModel):
    id: int
    name: str
    descripton: str
    price: float
    time: int
    image: str


class Order(BaseModel):
    id: int
    client_name: str
    service_id: int
    specialist_id: int
    time: datetime

class Specialist(BaseModel):
    id: int
    name: str
    avatar: str
    orders: Optional[List[Order]]
        
    
    
        


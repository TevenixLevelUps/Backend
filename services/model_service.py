from pydantic import BaseModel

class Service(BaseModel):
    name: str
    descripton: str
    price: float
    time: int
    image: str
    
    class Config:
        orm_mode = True
    
    
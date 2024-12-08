from pydantic import BaseModel

class Specialist(BaseModel):
    name: str
    avatar: str    
    
    class Config:
        orm_mode = True
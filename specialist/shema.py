from pydantic import BaseModel
from typing import Optional, Any

class BaseSpecialist(BaseModel):
    last_name: str
    first_name: str


class CreateSpecialist(BaseSpecialist):
    avatar: bytes | None = None

class UpdateSpecialist(CreateSpecialist):
    pass

class Specialist(CreateSpecialist):
    avatar_base64: Optional[Any]
    id: int

    class Config:
        orm_mode = True


class SpecialistRespon(BaseSpecialist):
    id: int
    avatar_base64: Any


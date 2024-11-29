from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


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
    model_config = ConfigDict(from_attributes=True)


class SpecialistRespon(BaseSpecialist):
    id: int
    avatar_base64: Any

from pydantic import BaseModel,ConfigDict
from typing import Optional

class SpecialistRegisterModel(BaseModel):
    name: str


class SpecialistResponseModel(BaseModel):
    id: int
    name: str
    avatar: str | None = None

    model_config = ConfigDict(from_attributes=True)

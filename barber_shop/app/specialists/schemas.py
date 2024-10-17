from uuid import UUID

from pydantic import BaseModel


class SSpecialistGet(BaseModel):
    id: UUID
    name: str
    avatar_id: UUID | None


class SSpecialistCreate(BaseModel):
    name: str

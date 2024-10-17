from uuid import UUID

from pydantic import BaseModel


class SSpecialist(BaseModel):
    id: UUID
    name: str
    avatar_id: UUID | None

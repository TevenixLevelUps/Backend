from uuid import UUID

from pydantic import BaseModel


class SSpecialistAvatar(BaseModel):
    id: UUID
    specialist_id: UUID
    image: bytes

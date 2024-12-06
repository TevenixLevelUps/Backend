from uuid import UUID

from pydantic import BaseModel


class SServiceImage(BaseModel):
    id: UUID
    service_id: UUID
    image: bytes

from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ServiceImages(Base):
    __tablename__ = 'service_images'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    service_id: Mapped[UUID] = mapped_column(unique=True, nullable=False)
    image: Mapped[bytes] = mapped_column(nullable=False)

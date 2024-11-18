from uuid import UUID

from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class SpecialistAvatars(Base):
    __tablename__ = 'specialist_avatars'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    specialist_id: Mapped[UUID] = mapped_column(unique=True, nullable=False)
    avatar: Mapped[bytes] = mapped_column(nullable=False)
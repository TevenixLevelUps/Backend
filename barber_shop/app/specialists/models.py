from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Specialists(Base):
    __tablename__ = 'specialists'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    avatar_id: Mapped[UUID] = mapped_column(nullable=True)

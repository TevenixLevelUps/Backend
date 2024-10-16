from datetime import time
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Services(Base):
    __tablename__ = 'services'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[Decimal] = mapped_column(nullable=False)
    lead_time: Mapped[time] = mapped_column(nullable=False)

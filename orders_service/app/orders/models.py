from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(nullable=False)
    service_id: Mapped[UUID] = mapped_column(nullable=False)
    specialist_id: Mapped[UUID] = mapped_column(nullable=False)
    order_time: Mapped[datetime] = mapped_column(nullable=False)

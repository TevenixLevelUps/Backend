from typing import TYPE_CHECKING

from sqlalchemy.types import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from sqlalchemy import String

if TYPE_CHECKING:
    from .orders import Orders


class Service(Base):

    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(150))
    price: Mapped[float] = mapped_column()
    execution_time: Mapped[int] = mapped_column()
    image: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    orders: Mapped["Orders"] = relationship(back_populates="service")

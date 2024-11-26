from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import LargeBinary

from .base import Base

if TYPE_CHECKING:
    from .orders import Orders


class Service(Base):

    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(150))
    price: Mapped[float] = mapped_column()
    execution_time: Mapped[int] = mapped_column()
    image: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    orders: Mapped["Orders"] = relationship(back_populates="service")

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import LargeBinary
from fastapi import UploadFile
from .base import Base

if TYPE_CHECKING:
    from .orders import  Orders


class Specialist(Base):
    first_name: Mapped[str | None] = mapped_column(
        String(20),
    )
    last_name: Mapped[str | None] = mapped_column(String(20))
    avatar : Mapped [bytes ] = mapped_column(LargeBinary,nullable=False)

    orders :Mapped["Orders"] = relationship(back_populates="specialist")
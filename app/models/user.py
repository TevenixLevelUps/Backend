from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .token import Token


class User(Base):
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_confirmed: Mapped[bool] = mapped_column(default=False)
    confirmation_code: Mapped[str] = mapped_column(unique=True, nullable=True)
    role: Mapped[str] = mapped_column(default="user")
    tokens: Mapped["Token"] = relationship(back_populates="user")
    reset_requests: Mapped[bool] = mapped_column(default=False)
    code_expiry_time: Mapped[datetime] = mapped_column(
        nullable=True, default=datetime.now() + timedelta(minutes=10)
    )
    reset_attempts: Mapped[int] = mapped_column(default=0)
    last_reset_attempts: Mapped[datetime] = mapped_column(default=datetime.now())

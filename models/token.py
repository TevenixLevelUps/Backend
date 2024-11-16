from typing import TYPE_CHECKING
from auth.config import ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import datetime, timedelta


if TYPE_CHECKING:
    from .user import User


class Token(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    access_token: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    token_type: Mapped[str] = mapped_column(nullable=False)
    expiry_time: Mapped[datetime] = mapped_column(
        nullable=False,
        default=lambda: datetime.utcnow()
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="tokens")

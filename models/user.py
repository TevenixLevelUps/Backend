from typing import TYPE_CHECKING


from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .token import Token


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_confirmed: Mapped[bool] = mapped_column(default=False)
    confirmation_code: Mapped[str] = mapped_column(unique=True, nullable=True)
    tokens: Mapped["Token"] = relationship("Token", back_populates="user")
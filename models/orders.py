from datetime import datetime


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped,mapped_column
from tomlkit import string

from .base import Base




class Orders(Base):
   client_name: Mapped[str] = mapped_column(string(25))
   service_id : Mapped[int] = mapped_column()
   specialist_id : Mapped[int] = mapped_column(ForeignKey('specialist_id'))
   time : Mapped[datetime] = mapped_column()
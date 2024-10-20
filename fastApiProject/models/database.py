from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase

import config

DATABASE_URL = config.DATABASE_URL

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine,future=True,expire_on_commit=False,class_=AsyncSession)


class Base(DeclarativeBase):
    pass

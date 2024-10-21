from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

DB_USER = settings.db.user
DB_PASS = settings.db.password
DB_HOST = settings.db.host
DB_PORT = settings.db.port
DB_NAME = settings.db.name


DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def session_getter() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

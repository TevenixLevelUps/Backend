from typing import AsyncGenerator

from app.config import settings
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DB_USER = settings.db.user
DB_PASS = settings.db.password
DB_HOST = settings.db.host
DB_PORT = settings.db.port
DB_NAME = settings.db.name

TEST_DB_USER = settings.testdb.user
TEST_DB_PASS = settings.testdb.password
TEST_DB_HOST = settings.testdb.host
TEST_DB_PORT = settings.testdb.port
TEST_DB_NAME = settings.testdb.name

if settings.mode.mode == "TEST":
    DATABASE_URL = f"postgresql+asyncpg://{TEST_DB_USER}:{TEST_DB_PASS}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
else:
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

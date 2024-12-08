from sqlalchemy.orm import DeclarativeBase   
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from config import settings
from sqlalchemy import NullPool

if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL 
    DATABASE_PARSMS = {}   

async_engine = create_async_engine(
    url=DATABASE_URL,
    **DATABASE_PARAMS
)

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
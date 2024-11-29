from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.database.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
            autocommit=False,
        )

    def get_scoped_session(self):
        session1 = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session1

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()

    async def session_dependency(self):
        async with self.session_factory() as session:
            yield session
            await session.close()


db_helper = DatabaseHelper(settings.Db_settings.url, settings.Db_settings.echo)

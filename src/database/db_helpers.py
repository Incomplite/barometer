from typing import AsyncGenerator

from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.config import project_config


class Base(DeclarativeBase):
    pass


class DatabaseHelper:
    def __init__(self, url: PostgresDsn, echo: bool = False):
        self.engine = create_async_engine(
            url=url.unicode_string(),
            echo=echo,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autocommit=False,
            autoflush=True,
        )

    async def get_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        db_session: AsyncSession = self.session_factory()
        try:
            yield db_session
        finally:
            await db_session.close()


db_helper = DatabaseHelper(
    url=project_config.db.database_url,
    echo=project_config.DB_ECHO_LOG,
)

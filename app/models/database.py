from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from app.config import settings
from app.utils.logger import get_logger


logger = get_logger("models.database")

engine = create_async_engine(settings.DB_URI, echo=settings.POSTGRES_ECHO)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False
)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator:
    """
    Генерирует сессию.

    :yield: AsyncGenerator
    """
    async with async_session() as session:
        logger.debug("ASYNC Pool: {pool}".format(pool=engine.pool.status()))
        yield session


async def init_db() -> None:
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


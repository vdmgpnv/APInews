from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError

from config import db_url


engine: AsyncEngine = create_async_engine(
   db_url, echo=False, echo_pool="debug", isolation_level="AUTOCOMMIT"
)
DBSession = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with DBSession() as session:
        try:
            yield session
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex
        else:
            await session.commit()
        finally:
            await session.close()

from sqlalchemy import Integer
from sqlalchemy.orm import (
    declared_attr, mapped_column, declarative_base
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id = mapped_column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

db_url = 'postgresql+asyncpg://techcore:techcore@db:5432/techcore'

engine = create_async_engine(db_url)

local_async_session = async_sessionmaker(engine, class_=AsyncSession)
SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)


async def get_session():
    async with local_async_session() as async_session:
        yield async_session

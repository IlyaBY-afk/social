from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from settings import settings


if settings.MODE == 'TEST':
    DB_URL = settings.TEST_DB_URL
    DB_PARAMS = {'poolclass': NullPool}
else:
    DB_URL = settings.DB_URL
    DB_PARAMS = {}


engine = create_async_engine(settings.DB_URL, **DB_PARAMS)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
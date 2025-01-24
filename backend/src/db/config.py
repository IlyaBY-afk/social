from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import AsyncGenerator

from src.db.manager import SqlDbManager
from src.models import User
from settings import settings


if settings.MODE == 'TEST':
    DB_URL = settings.TEST_DB_URL
    DB_PARAMS = {'poolclass': NullPool}
else:
    DB_URL = settings.DB_URL
    DB_PARAMS = {}

db_manager = SqlDbManager(
    DB_URL, DB_PARAMS
)
async_session_maker = async_sessionmaker(db_manager.engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

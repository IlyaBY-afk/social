import pytest
import json
from sqlalchemy import insert
from httpx import AsyncClient, ASGITransport

from src.db.config import async_session_maker, db_manager
from src.models import User, Base
from src.app import app
from settings import settings


@pytest.fixture(scope='session', autouse=True)
async def prepare_db():
    assert settings.MODE == 'TEST'

    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f'tests/mock_{model}.json', 'r') as f:
            return json.load(f)
        
    users = open_mock_json('users')

    async with async_session_maker() as session:
        add_users = insert(User).values(users)

        await session.execute(add_users)
        await session.commit()
    

@pytest.fixture(scope='function')
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        yield client
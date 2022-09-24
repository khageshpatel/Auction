import pytest
import sys
import asyncio
from typing import Generator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.db.connector import Base, async_session
from app.db.user_dal import UserDal
from typing import AsyncGenerator
import pytest_asyncio
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from app.models.user import User
from app.models.auction import Auction, AuctionBid
from app.models.product import Product


@pytest_asyncio.fixture(scope="session")
def event_loop(request) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def db_session() -> AsyncSession:
    """Create an instance of db session."""
    engine  = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost/auction_test", future=True, echo=True)
    async with engine.begin() as connection:
        # This can be done intelligently.
        await connection.run_sync(AuctionBid.__table__.drop)
        await connection.run_sync(Auction.__table__.drop)
        await connection.run_sync(Product.__table__.drop)
        await connection.run_sync(User.__table__.drop)
        await connection.run_sync(Base.metadata.create_all)
        async with async_session(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()

@pytest_asyncio.fixture()
async def user_dal(db_session: AsyncSession) -> UserDal:
    return UserDal(db_session)

@pytest_asyncio.fixture()
def override_get_user_dal(user_dal: UserDal):
    async def _override_get_user_dal():
        yield user_dal

    return _override_get_user_dal


@pytest_asyncio.fixture()
def app(override_get_user_dal):
    from app.db.dependencies import get_user_dal
    from app.main import app

    app.dependency_overrides[get_user_dal] = override_get_user_dal
    return app

@pytest_asyncio.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

from app.core.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

sync_engine = create_engine(settings.SQLALCHEMY_DATABASE_URI.replace('+asyncpg', ''), pool_pre_ping=True)
sync_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

import sys
from os.path import dirname, abspath, join

BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
sys.path.insert(0, BASE_DIR)
DB_PATH = join(BASE_DIR, "weather.db")

URL = f"sqlite+aiosqlite:///{DB_PATH}"

engine = create_async_engine(url=URL, echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

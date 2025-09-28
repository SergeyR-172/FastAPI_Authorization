from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")


async_engine = create_async_engine(DATABASE_URL)


async def get_async_db():
    async with AsyncSession(bind=async_engine) as db:
        try:
            yield db
        finally:
            await db.close()

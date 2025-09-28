import asyncio
from database import async_engine
from models.base import Base
from models.user import User

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())
import asyncio
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession,
    async_scoped_session
)
from sqlalchemy.orm import sessionmaker
from beringbankdb import Base

#engine = create_async_engine("sqlite+aiosqlite:///banking.db", future=True)
DATABASE_URL = "sqlite+aiosqlite:///app/banking.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async def create_tables():
    async with engine.begin() as conn:
        print(Base)
        await conn.run_sync(Base.metadata.create_all)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def run():
    # Create tables
    await create_tables()
    async with AsyncSessionLocal() as session:  
        # Your asynchronous operations go here
        print(session)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(run())
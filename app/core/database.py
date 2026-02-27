from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, pool_size=1000, max_overflow=-1, connect_args={"timeout": 60})
session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def database():
    async with session_maker() as session:
        yield session

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.database.database import engine
from app.database.utils import populate_database
from app.models.table_model import Table


async def init_data():
    async with async_sessionmaker(engine)() as session:
        result = await session.execute(select(Table).limit(1))
        if result.scalars().first():
            return
        await populate_database(session)

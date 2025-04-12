from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.database import AsyncSessionLocal, Base, engine
from app.database.utils import populate_database
from app.routers import reservation_routers, table_routers
from app.scripts.seed import init_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_data()
    yield


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     async with AsyncSessionLocal() as session:
#         await populate_database(session)
#     yield


app = FastAPI(lifespan=lifespan)

app.include_router(table_routers.router)
app.include_router(reservation_routers.router)

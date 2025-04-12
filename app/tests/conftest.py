import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import (  # type: ignore
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.database.database import Base, get_db
from app.models.reservation_model import Reservation  # noqa
from app.models.table_model import Table  # noqa

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


# TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture
async def session(engine):
    async with async_sessionmaker(engine)() as session:
        yield session


@pytest.fixture
async def app(engine):
    app = FastAPI()

    async def override_get_db():
        async with async_sessionmaker(engine)() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    from main import app as main_app

    app.include_router(main_app.router)

    return app


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def test_tables(session: AsyncSession):
    await session.execute(delete(Table))
    await session.commit()
    table1 = Table(name="Table1", seats=2, location="Location1")
    table2 = Table(name="Table2", seats=3, location="Location2")

    session.add_all([table1, table2])
    await session.commit()


@pytest.fixture
async def test_reservations(session: AsyncSession, test_tables):
    await session.execute(delete(Reservation))
    await session.commit()
    reservation1 = Reservation(
        customer_name="Test Customer1", table_id=1, duration_minutes=60
    )
    reservation2 = Reservation(
        customer_name="Test Customer2", table_id=1, duration_minutes=120
    )

    session.add_all([reservation1, reservation2])
    await session.commit()

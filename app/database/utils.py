from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reservation_model import Reservation
from app.models.table_model import Table


async def populate_database(db: AsyncSession):

    table1 = Table(name="Table 1", seats=2, location="seats 1")
    table2 = Table(name="Table 2", seats=2, location="seats 2")
    table3 = Table(name="Table 3", seats=2, location="seats 3")
    table4 = Table(name="Table 4", seats=2, location="seats 4")
    table5 = Table(name="Table 5", seats=2, location="seats 5")

    db.add_all([table1, table2, table3, table4, table5])
    await db.flush()

    reservation1 = Reservation(
        customer_name="test 1", table_id=table1.id, duration_minutes=120
    )
    reservation2 = Reservation(
        customer_name="test 2", table_id=table2.id, duration_minutes=180
    )
    reservation3 = Reservation(
        customer_name="test 3", table_id=table3.id, duration_minutes=60
    )

    db.add_all([reservation1, reservation2, reservation3])
    await db.commit()

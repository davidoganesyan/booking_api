from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.database.database import get_db
from app.models.reservation_model import Reservation
from app.models.table_model import Table
from app.schemas.reservation_shemas import ReservationCreate, ReservationResponse

router = APIRouter(tags=["Reservations"])


@router.get("/reservations/", response_model=List[ReservationResponse])
async def get_reservations(db: AsyncSession = Depends(get_db)):  # noqa: B008
    return (
        (await db.execute(select(Reservation).options(joinedload(Reservation.table))))
        .scalars()
        .unique()
        .all()
    )


@router.post("/reservations/", response_model=ReservationResponse)
async def create_reservation(
    reservation_data: ReservationCreate,
    db: AsyncSession = Depends(get_db),  # noqa: B008
):
    table = await db.get(Table, reservation_data.table_id)
    if not table:
        raise HTTPException(404, "No table with that ID")

    new_start = reservation_data.reservation_time
    new_end = new_start + timedelta(minutes=reservation_data.duration_minutes)

    # existing = await db.execute(
    #     select(Reservation).where(
    #         Reservation.table_id == reservation_data.table_id,
    #         and_(
    #             # Конец существующей резервации > начала новой
    #             func.datetime(
    #                 Reservation.reservation_time,
    #                 text("'+' || duration_minutes || ' minutes'"),
    #             )
    #             > new_start,
    #             # Начало существующей резервации < конца новой
    #             Reservation.reservation_time < new_end,
    #         ),
    #     )
    # )

    existing = await db.execute(
        select(Reservation).where(
            Reservation.table_id == reservation_data.table_id,
            and_(
                (
                    Reservation.reservation_time
                    + func.make_interval(0, 0, 0, 0, 0, Reservation.duration_minutes)
                )
                > new_start,
                Reservation.reservation_time < new_end,
            ),
        )
    )

    if existing.scalars().first():
        raise HTTPException(400, "Table already reserved")

    new_reservation = Reservation(**reservation_data.model_dump())
    db.add(new_reservation)
    await db.commit()
    await db.refresh(new_reservation)
    return new_reservation


@router.delete("/reservations/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    reservation_id: int, db: AsyncSession = Depends(get_db)  # noqa: B008
):
    reservation = await db.get(Reservation, reservation_id)

    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reservation with ID {reservation_id} not found",
        )

    await db.delete(reservation)
    await db.commit()

    return status.HTTP_204_NO_CONTENT

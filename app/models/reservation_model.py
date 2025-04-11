from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Reservation(Base):
    __tablename__ = "reservation"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(String)
    table_id: Mapped[int] = mapped_column(ForeignKey("table.id"))
    reservation_time: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    duration_minutes: Mapped[int] = mapped_column(Integer)

    table: Mapped["Table"] = relationship(  # type: ignore # noqa
        "Table", back_populates="reservation", lazy="joined"
    )

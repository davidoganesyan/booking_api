from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Table(Base):
    __tablename__ = "table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    seats: Mapped[int] = mapped_column(Integer)
    location: Mapped[str] = mapped_column(String)

    reservation: Mapped["Reservation"] = relationship(  # type: ignore # noqa
        "Reservation", back_populates="table", cascade="all, delete"
    )

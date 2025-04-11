from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.table_shemas import TableResponse


class ReservationResponse(BaseModel):
    id: int
    customer_name: str
    reservation_time: datetime
    duration_minutes: int
    table: TableResponse

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")},
        json_schema_extra={
            "example": {
                "id": 1,
                "customer_name": "Test 1",
                "reservation_time": "2025-04-12 12:00:00",
                "duration_minutes": 120,
                "table": {
                    "id": 1,
                    "name": "Table 1",
                    "seats": 2,
                    "location": "seats 1",
                },
            },
        },
    )


class ReservationCreate(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "customer_name": "Test customer",
                "table_id": 1,
                "reservation_time": "2025-04-12 12:00:00",
                "duration_minutes": 90,
            }
        },
    )

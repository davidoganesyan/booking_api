from pydantic import BaseModel, ConfigDict, Field


class TableResponse(BaseModel):
    id: int
    name: str
    seats: int
    location: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {"id": 1, "name": "Table", "seats": 6, "location": "balcony"}
        },
    )


class TableCreate(BaseModel):
    name: str = Field(..., description="Table name (unique)")
    seats: int = Field(..., gt=0, description="Number of seats")
    location: str = Field(..., description="Table location")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"name": "Table", "seats": 6, "location": "balcony"}
        }
    )

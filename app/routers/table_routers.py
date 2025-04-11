from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.models.table_model import Table
from app.schemas.table_shemas import TableCreate, TableResponse

router = APIRouter(tags=["Tables"])


@router.get("/tables/", response_model=List[TableResponse])
async def get_tables(db: AsyncSession = Depends(get_db)):  # noqa: B008
    return (await db.execute(select(Table))).scalars().all()


@router.post(
    "/tables/",
    response_model=TableResponse,
    status_code=status.HTTP_201_CREATED,
    responses={201: {"description": "Table was created successfully"}},
)
async def create_table(
    table_data: TableCreate, db: AsyncSession = Depends(get_db)  # noqa: B008
):
    existing_table = await db.execute(
        select(Table).where(Table.name == table_data.name)
    )
    if existing_table.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Table with name '{table_data.name}' already exists",
        )

    new_table = Table(**table_data.model_dump())
    db.add(new_table)
    await db.commit()
    await db.refresh(new_table)
    return new_table


@router.delete("/tables/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(table_id: int, db: AsyncSession = Depends(get_db)):  # noqa: B008
    table = await db.get(Table, table_id)

    if not table:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Table with ID {table_id} not found",
        )

    await db.delete(table)
    await db.commit()

    return status.HTTP_204_NO_CONTENT

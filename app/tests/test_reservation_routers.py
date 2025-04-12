import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_reservations(client: AsyncClient, test_tables, test_reservations):
    response = await client.get("/reservations/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["customer_name"] == "Test Customer1"


@pytest.mark.asyncio
async def test_post_reservations(client: AsyncClient, test_tables, test_reservations):
    response = await client.post(
        "/reservations/",
        json={
            "customer_name": "Test customer",
            "duration_minutes": 90,
            "reservation_time": "2025-04-12 12:00:00",
            "table_id": 1,
        },
    )
    assert response.status_code == 200
    assert response.json()["id"] == 3
    reservation_on_same_time = await client.post(
        "/reservations/",
        json={
            "customer_name": "Test customer",
            "duration_minutes": 61,
            "reservation_time": "2025-04-12 13:00:00",
            "table_id": 1,
        },
    )
    assert reservation_on_same_time.status_code == 400
    assert "already reserved" in reservation_on_same_time.json()["detail"]


@pytest.mark.asyncio
async def test_delete_reservations(client: AsyncClient, test_tables, test_reservations):
    response = await client.delete("/reservations/2")
    assert response.status_code == 204
    bad_request = await client.delete("/reservations/24")
    assert bad_request.status_code == 404
    assert "not found" in bad_request.json()["detail"]
    check_response = await client.get("/reservations/")
    assert len(check_response.json()) == 1

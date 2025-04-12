import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_tables(client: AsyncClient, test_tables):
    response = await client.get("/tables/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Table1"


@pytest.mark.asyncio
async def test_post_tables(client: AsyncClient, test_tables):
    response = await client.post(
        "/tables/", json={"name": "Table3", "seats": "3", "location": "Location3"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Table3"

    bad_request = await client.post(
        "/tables/", json={"name": "Table2", "seats": "3", "location": "Location3"}
    )
    assert bad_request.status_code == 400
    assert "already exists" in bad_request.json()["detail"]


@pytest.mark.asyncio
async def test_delete_tables(client: AsyncClient, test_tables):
    response = await client.delete("/tables/2")
    assert response.status_code == 204
    bad_request = await client.delete("/tables/24")
    assert bad_request.status_code == 404
    assert "not found" in bad_request.json()["detail"]

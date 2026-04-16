import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_categories(client: AsyncClient):
    response = await client.get("/v1/catalog/categories")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert len(data["categories"]) == 4

@pytest.mark.asyncio
async def test_get_services(client: AsyncClient):
    response = await client.get("/v1/catalog/services")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) or "items" in data
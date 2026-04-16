import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_order_success(client: AsyncClient):
    response = await client.post("/v1/orders/", json={
        "service_id": 1,
        "client_id": 4,
        "address": "Test Address",
        "scheduled_at": "2026-04-20T14:00:00",
        "description": "Test order",
        "estimated_hours": 1,
        "hourly_rate": 1000,
        "materials_cost": 500,
        "urgency_coefficient": 0
    })
    assert response.status_code == 200
    data = response.json()
    assert "order_id" in data
    assert data["status"] == "New"

@pytest.mark.asyncio
async def test_create_order_invalid_service(client: AsyncClient):
    response = await client.post("/v1/orders/", json={
        "service_id": 99999,
        "client_id": 4,
        "address": "Test",
        "scheduled_at": "2026-04-20T14:00:00",
        "description": "Test",
        "estimated_hours": 1,
        "hourly_rate": 1000,
        "materials_cost": 0,
        "urgency_coefficient": 0
    })
    assert response.status_code == 404
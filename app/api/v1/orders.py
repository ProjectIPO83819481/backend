from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field
from datetime import datetime
from app.api.deps import get_db
from app.models.models import Order, Status
from app.models.service import Service
from sqlalchemy import select

from app.services.orders.cost_calculator import calculate_order_cost

router = APIRouter(tags=["orders"])

class CreateOrderRequest(BaseModel):
    service_id: int
    client_id: int
    address: str
    scheduled_at: datetime
    description: str
    
    estimated_hours: int = Field(default=1, ge=0, description="Time to complete (hours)")
    hourly_rate: float = Field(default=0.0, ge=0, description="Hourly rate")
    materials_cost: float = Field(default=0.0, ge=0, description="Materials cost")
    urgency_coefficient: float = Field(default=0.0, ge=0, description="Urgency surcharge")


@router.post("/orders/", response_model=dict)
async def create_order(order_data: CreateOrderRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Service).where(Service.service_id == order_data.service_id))
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="The service was not found in the catalog")

    try:
        final_cost = calculate_order_cost(
            base_price=float(service.base_price),
            hours=order_data.estimated_hours,
            rate_per_hour=order_data.hourly_rate,
            materials=order_data.materials_cost,
            urgency_coeff=order_data.urgency_coefficient
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if final_cost <= 0:
        raise HTTPException(status_code=400, detail="The total cost must be greater than 0")

    new_order = Order(
        client_id=order_data.client_id,
        service_id=order_data.service_id,
        address=order_data.address,
        scheduled_at=order_data.scheduled_at,
        description=order_data.description,
        status=Status.NEW,
        base_cost=float(service.base_price),  
        final_cost=final_cost
    )

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    return {
        "order_id": new_order.order_id,
        "status": new_order.status.value,
        "base_cost": float(new_order.base_cost),
        "final_cost": float(new_order.final_cost)
    }
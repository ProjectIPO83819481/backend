from ...models.models import Order
from ...models.base import Base
from ...models.service import ServiceCategory
from ...services.service_functions import get_catalog_services
from sqlalchemy import DateTime
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
class User_Request(Base):
    service_number: int
    address: str
    needs_date: DateTime
    needs_time: DateTime
    description: str
async def user_create_order(db: Session,
    category: Optional[ServiceCategory] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_active: bool = True) -> User_Request:

    
    service_category_list = get_catalog_services()
    print("Enter category num")
    category_number: int = input()
    print("Enter address")
    address: str = input()
    print("Enter needs date to visit")
    needs_date: DateTime = input()
    print("Enter needs time to visit")
    needs_time: DateTime = input()
    print("Enter description of yours problem")
    description: str = input()

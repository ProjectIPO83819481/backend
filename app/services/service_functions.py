from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from models.service import Service, ServiceCategory
from utils.subcategories import SUBCATEGORIES

def filtration_on_category(
    db: Session, 
    category: ServiceCategory,
    is_active: bool = True
) -> List[Service]:

    query = db.query(Service).filter(
        Service.category_name == category,
        Service.is_active == is_active
    )
    
    return query.all()


def filtration_on_category_with_subcategories(
    db: Session,
    category: ServiceCategory,
    subcategories: Optional[List[str]] = None,
    is_active: bool = True
) -> List[Service]:

    query = db.query(Service).filter(
        Service.category_name == category,
        Service.is_active == is_active
    )
    
    if subcategories:
        conditions = [
            Service.description.ilike(f"%{sub}%") 
            for sub in subcategories
        ]
        query = query.filter(or_(*conditions))
    
    return query.all()


def filtration_with_price_range(
    db: Session,
    category: Optional[ServiceCategory] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_active: bool = True
) -> List[Service]:
    
    query = db.query(Service).filter(Service.is_active == is_active)
    
    if category:
        query = query.filter(Service.category_name == category)
    
    if min_price is not None:
        query = query.filter(Service.base_price >= min_price)
    
    if max_price is not None:
        query = query.filter(Service.base_price <= max_price)
    
    return query.all()
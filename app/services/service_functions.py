from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Tuple
from models.service import Service, ServiceCategory, Photo
from utils.subcategories import SUBCATEGORIES
from sqlalchemy import select, delete, update


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


async def get_catalog_services(
    db: AsyncSession,
    category: Optional[ServiceCategory] = None,
    subcategory: Optional[str] = None,
    search_query: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = "popularity",
    sort_order: str = "desc",
    skip: int = 0,
    limit: int = 20,
    is_active: bool = True
) -> Tuple[List[Service], int]:

    from sqlalchemy import select, func

    query = select(Service).where(Service.is_active == is_active)

    if category:
        query = query.where(Service.category_name == category)

    if subcategory:
        query = query.where(Service.subcategory == subcategory)

    if min_price is not None:
        query = query.where(Service.base_price >= min_price)
    
    if max_price is not None:
        query = query.where(Service.base_price <= max_price)

    if search_query:
        search_term = f"%{search_query}%"
        query = query.where(
            or_(
                Service.name.ilike(search_term),
                Service.description.ilike(search_term),
                Service.required_materials.ilike(search_term)
            )
        )

    count_query = select(func.count()).select_from(Service).where(Service.is_active == is_active)
    if category:
        count_query = count_query.where(Service.category_name == category)
    if subcategory:
        count_query = count_query.where(Service.subcategory == subcategory)
    if min_price is not None:
        count_query = count_query.where(Service.base_price >= min_price)
    if max_price is not None:
        count_query = count_query.where(Service.base_price <= max_price)
    if search_query:
        search_term = f"%{search_query}%"
        count_query = count_query.where(
            or_(
                Service.name.ilike(search_term),
                Service.description.ilike(search_term),
                Service.required_materials.ilike(search_term)
            )
        )
    
    result = await db.execute(count_query)
    total_count = result.scalar()
    
    if sort_by == "price":
        sort_column = Service.base_price
    elif sort_by == "rating":
        sort_column = Service.rating
    elif sort_by == "newest":
        sort_column = Service.created_at
    else:  # popularity
        sort_column = Service.popularity_score
    
    if sort_order.lower() == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    services = result.scalars().unique().all()
    
    return services, total_count


async def search_services(
    db: AsyncSession,
    search_query: str,
    limit: int = 50,
    is_active: bool = True
) -> List[Service]:
    
    search_term = f"%{search_query}%"
    query = select(Service).where(
        and_(
            Service.is_active == is_active,
            or_(
                Service.name.ilike(search_term),
                Service.description.ilike(search_term),
                Service.required_materials.ilike(search_term)
            )
        )
    ).order_by(
        desc(Service.popularity_score)
    ).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().unique().all()


async def get_service_by_id(
    db: AsyncSession,
    service_id: int,
    is_active_only: bool = True
) -> Optional[Service]:
    query = select(Service).where(Service.service_id == service_id)
    
    if is_active_only:
        query = query.where(Service.is_active == True)
    
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_services_by_category(
    db: AsyncSession,
    category: ServiceCategory,
    limit: int = 50,
    is_active: bool = True
) -> List[Service]:
    
    query = select(Service).where(
        and_(
            Service.category_name == category,
            Service.is_active == is_active
        )
    ).order_by(desc(Service.popularity_score)).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().unique().all()


async def get_similar_services(
    db: AsyncSession,
    service_id: int,
    limit: int = 5,
    is_active: bool = True
) -> List[Service]:

    service = await get_service_by_id(db, service_id, is_active_only=False)
    if not service:
        return []

    query = select(Service).where(
        and_(
            Service.service_id != service_id,
            Service.category_name == service.category_name,
            Service.is_active == is_active
        )
    ).order_by(
        desc(Service.popularity_score)
    ).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().unique().all()


async def get_top_rated_services(
    db: AsyncSession,
    limit: int = 10,
    min_reviews: int = 1,
    is_active: bool = True
) -> List[Service]:
    query = select(Service).where(
        and_(
            Service.is_active == is_active,
            Service.total_reviews >= min_reviews
        )
    ).order_by(
        desc(Service.rating)
    ).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().unique().all()


async def get_trending_services(
    db: AsyncSession,
    limit: int = 10,
    is_active: bool = True
) -> List[Service]:
    query = select(Service).where(
        Service.is_active == is_active
    ).order_by(
        desc(Service.popularity_score)
    ).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().unique().all()


async def add_photo_to_service(
    db: AsyncSession,
    service_id: int,
    image_url: str,
    description: Optional[str] = None
) -> Photo:
    photo = Photo(
        service_id=service_id,
        image_url=image_url,
        description=description
    )
    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    return photo


async def remove_photo(
    db: AsyncSession,
    photo_id: int
) -> bool:
    query = delete(Photo).where(Photo.photo_id == photo_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0


async def update_service_rating(
    db: AsyncSession,
    service_id: int,
    new_rating: float,
    increment_reviews: int = 1
) -> Optional[Service]:

    service = await get_service_by_id(db, service_id, is_active_only=False)
    if not service:
        return None
    
    # Calculate new average rating
    current_total = service.total_reviews * service.rating
    new_total_reviews = service.total_reviews + increment_reviews
    new_avg_rating = (current_total + (new_rating * increment_reviews)) / new_total_reviews
    
    # Update service
    update_query = update(Service).where(
        Service.service_id == service_id
    ).values(
        rating=new_avg_rating,
        total_reviews=new_total_reviews
    )
    
    await db.execute(update_query)
    await db.commit()
    
    return await get_service_by_id(db, service_id, is_active_only=False)


async def update_service_popularity(
    db: AsyncSession,
    service_id: int,
    popularity_increment: float
) -> Optional[Service]:

    service = await get_service_by_id(db, service_id, is_active_only=False)
    if not service:
        return None
    
    new_popularity = max(0, service.popularity_score + popularity_increment)
    
    update_query = update(Service).where(
        Service.service_id == service_id
    ).values(
        popularity_score=new_popularity
    )
    
    await db.execute(update_query)
    await db.commit()
    
    return await get_service_by_id(db, service_id, is_active_only=False)

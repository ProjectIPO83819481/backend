from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from models.schemas import (
    ServiceCatalogResponse,
    ServiceDetailResponse,
    CatalogListResponse,
    CategoryResponse,
    CategoryListResponse,
)
from models.service import ServiceCategory
from services.service_functions import (
    get_catalog_services,
    search_services,
    get_service_by_id,
    get_services_by_category,
    get_similar_services,
    get_top_rated_services,
    get_trending_services,
)
from utils.subcategories import SUBCATEGORIES
from ..deps import get_db
router = APIRouter(prefix="/catalog", tags=["catalog"])



def get_service_category_enum(category_str: str) -> ServiceCategory:
    for cat in ServiceCategory:
        if cat.value == category_str:
            return cat
    raise ValueError(f"Invalid category: {category_str}")


@router.get("/services", response_model=CatalogListResponse)
async def list_services(
    category: Optional[str] = Query(None, description="Filter by category"),
    subcategory: Optional[str] = Query(None, description="Filter by subcategory"),
    search: Optional[str] = Query(None, description="Search by name, description, or materials"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    sort_by: str = Query("popularity", regex="^(price|rating|popularity|newest)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    category_enum = None
    if category:
        try:
            category_enum = get_service_category_enum(category)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    
    services, total = await get_catalog_services(
        db=db,
        category=category_enum,
        subcategory=subcategory,
        search_query=search,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        sort_order=sort_order,
        skip=skip,
        limit=limit,
    )
    
    return CatalogListResponse(
        total=total,
        skip=skip,
        limit=limit,
        items=[ServiceCatalogResponse.from_attributes(s) for s in services],
    )


@router.get("/services/search", response_model=List[ServiceCatalogResponse])
async def search_catalog(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    services = await search_services(db, q, limit=limit)
    return [ServiceCatalogResponse.from_attributes(s) for s in services]


@router.get("/services/{service_id}", response_model=ServiceDetailResponse)
async def get_service_details(
    service_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = await get_service_by_id(db, service_id)
    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )
    
    return ServiceDetailResponse.from_attributes(service)


@router.get("/services/{service_id}/similar", response_model=List[ServiceCatalogResponse])
async def get_similar(
    service_id: int,
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    service = await get_service_by_id(db, service_id)
    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )
    
    similar = await get_similar_services(db, service_id, limit=limit)
    return [ServiceCatalogResponse.from_attributes(s) for s in similar]


@router.get("/categories", response_model=CategoryListResponse)
async def list_categories():
    categories = []
    
    for category_str, subcats in SUBCATEGORIES.items():
        descriptions = {
            "Cleaning": "Professional cleaning services for your home and office",
            "Plumbing": "Professional plumbing installation, repair and maintenance",
            "Electrical": "Professional electrical services and installations",
            "Repairs": "General home repairs and restoration services",
        }
        
        categories.append(
            CategoryResponse(
                category=category_str,
                description=descriptions.get(category_str, ""),
                subcategories=subcats,
            )
        )
    
    return CategoryListResponse(categories=categories)


@router.get("/categories/{category}/subcategories", response_model=List[str])
async def get_subcategories(
    category: str,
):
    subcategories = SUBCATEGORIES.get(category)
    if subcategories is None:
        raise HTTPException(
            status_code=404,
            detail=f"Category '{category}' not found",
        )
    
    return subcategories


@router.get("/categories/{category}/services", response_model=List[ServiceCatalogResponse])
async def get_category_services(
    category: str,
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    try:
        category_enum = get_service_category_enum(category)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Category '{category}' not found")
    
    services = await get_services_by_category(db, category_enum, limit=limit)
    return [ServiceCatalogResponse.from_attributes(s) for s in services]


@router.get("/top-rated", response_model=List[ServiceCatalogResponse])
async def get_top_rated(
    limit: int = Query(10, ge=1, le=50),
    min_reviews: int = Query(1, ge=0, description="Minimum number of reviews"),
    db: AsyncSession = Depends(get_db),
):
    services = await get_top_rated_services(db, limit=limit, min_reviews=min_reviews)
    return [ServiceCatalogResponse.from_attributes(s) for s in services]


@router.get("/trending", response_model=List[ServiceCatalogResponse])
async def get_trending(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    services = await get_trending_services(db, limit=limit)
    return [ServiceCatalogResponse.from_attributes(s) for s in services]

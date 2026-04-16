from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum


class ServiceCategoryEnum(str, Enum):
    CLEANING = "Cleaning"
    PLUMBING = "Plumbing"
    ELECTRICAL = "Electrical"
    REPAIRS = "Repairs"


class PhotoBase(BaseModel):
    image_url: str
    description: Optional[str] = None


class PhotoCreate(PhotoBase):
    pass


class PhotoResponse(PhotoBase):
    photo_id: int
    service_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ServiceBase(BaseModel):
    name: str
    category_name: ServiceCategoryEnum
    subcategory: Optional[str] = None
    description: str
    base_price: float
    price_range_max: Optional[float] = None
    avg_duration_minutes: int
    required_materials: Optional[str] = None


class ServiceCreate(ServiceBase):
    user_id: int


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    subcategory: Optional[str] = None
    base_price: Optional[float] = None
    price_range_max: Optional[float] = None
    avg_duration_minutes: Optional[int] = None
    required_materials: Optional[str] = None


class ServicePriceUpdate(BaseModel):
    base_price: float
    price_range_max: Optional[float] = None


class ServiceDescriptionUpdate(BaseModel):
    description: str


class ServiceCatalogResponse(BaseModel):
    service_id: int
    name: str
    category_name: ServiceCategoryEnum
    subcategory: Optional[str] = None
    description: str
    base_price: float
    price_range_max: Optional[float] = None
    avg_duration_minutes: int
    rating: float = Field(ge=0, le=5)
    total_reviews: int
    popularity_score: float
    photos: List[PhotoResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ServiceDetailResponse(ServiceCatalogResponse):
    required_materials: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CatalogFilterRequest(BaseModel):
    category: Optional[ServiceCategoryEnum] = None
    subcategory: Optional[str] = None
    search: Optional[str] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    sort_by: Optional[str] = Field("popularity", pattern="^(price|rating|popularity|newest)$")
    sort_order: Optional[str] = Field("desc", pattern="^(asc|desc)$")
    skip: int = Field(0, ge=0)
    limit: int = Field(20, ge=1, le=100)


class CatalogListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[ServiceCatalogResponse]


class CategoryResponse(BaseModel):
    category: str
    description: str
    subcategories: List[str]


class CategoryListResponse(BaseModel):
    categories: List[CategoryResponse]

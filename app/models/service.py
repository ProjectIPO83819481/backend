import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum as SQLEnum, ForeignKey, Numeric, Float
from sqlalchemy.orm import relationship

from .base import Base


class ServiceCategory(enum.Enum):
    CLEANING = "Cleaning"
    PLUMBING = "Plumbing"
    ELECTRICAL = "Electrical"
    REPAIRS = "Repairs"

class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    category_name = Column(SQLEnum(ServiceCategory), nullable=False, index=True)
    subcategory = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=False)
    base_price = Column(Numeric(10, 2), nullable=False)
    price_range_max = Column(Numeric(10, 2), nullable=True)
    avg_duration_minutes = Column(Integer, nullable=False)
    required_materials = Column(Text, nullable=True)
    rating = Column(Float, default=0.0, nullable=False)
    total_reviews = Column(Integer, default=0, nullable=False)
    popularity_score = Column(Float, default=0.0, nullable=False)
    photos = relationship("Photo", back_populates="service", cascade="all, delete-orphan")
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Photo(Base):
    __tablename__ = "service_photos"

    photo_id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.service_id"), nullable=False, index=True)
    image_url = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    service = relationship("Service", back_populates="photos")
    created_at = Column(DateTime, default=datetime.utcnow)
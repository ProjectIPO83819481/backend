from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum as SQLEnum, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from . import Base
import enum

class ServiceCategory(enum.Enum):
    CLEANING = "Cleaning"
    PLUMBING = "Plumbing"
    ELECTRICAL = "Electrical"
    REPAIRS = "Repairs"

class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    category_name = Column(SQLEnum(ServiceCategory), nullable=False, index=True)
    description = Column(Text, nullable=False)
    base_price = Column(Numeric(10, 2), nullable=False)
    price_range_max = Column(Numeric(10, 2), nullable=True)
    avg_duration_minutes = Column(Integer, nullable=False)
    required_materials = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
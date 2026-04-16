import enum
from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Numeric, Enum as SQLEnum, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from .base import Base

class Role(enum.Enum):
    CLIENT = "Client"
    EXECUTOR = "Executor"
    ADMIN = "Admin"

class Status(enum.Enum):
    NEW = "New"
    ACCEPTED = "Accepted"
    IN_PROGRESS = "In_Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class AdditionalWorkRequestStatuses(enum.Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class User(Base):
    __tablename__ = 'users'
                            
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(Role), nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    photo_url = Column(String(255), nullable=True)
    is_suspended = Column(Boolean, default=False, nullable=False)
    suspended_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    services = relationship("Service", back_populates="user", foreign_keys="Service.user_id", cascade="all, delete-orphan")
    orders_as_client = relationship("Order", foreign_keys="Order.client_id", back_populates="client", cascade="all, delete-orphan")
    orders_as_executor = relationship("Order", foreign_keys="Order.executor_id", back_populates="executor")
    additional_work_responses = relationship("AdditionalWork", back_populates="responder", cascade="all, delete-orphan")
    cancelled_orders = relationship("Order", foreign_keys="Order.cancelled_by_user_id", back_populates="cancelled_by_user")


class Order(Base):
    __tablename__ = 'orders'                       

    order_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    executor_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    service_id = Column(Integer, ForeignKey("services.service_id"), nullable=False)
    cancelled_by_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    status = Column(SQLEnum(Status), nullable=False, index=True, default=Status.NEW)
    address = Column(String(255), nullable=True)
    scheduled_at = Column(DateTime, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    cancellation_reason = Column(Text, nullable=True)
    review_comment = Column(Text, nullable=True)
    review_created_at = Column(DateTime, nullable=True)
    review_executor_response = Column(String(255), nullable=True)
    base_cost = Column(Numeric(precision=10, scale=2), nullable=False)
    final_cost = Column(Numeric(precision=10, scale=2), nullable=False)
    client = relationship("User", foreign_keys=[client_id], back_populates="orders_as_client")
    executor = relationship("User", foreign_keys=[executor_id], back_populates="orders_as_executor")
    service = relationship("Service", back_populates="orders")
    cancelled_by_user = relationship("User", foreign_keys=[cancelled_by_user_id], back_populates="cancelled_orders")
    additional_work_requests = relationship("AdditionalWork", back_populates="order", cascade="all, delete-orphan")
    __table_args__ = (
        CheckConstraint("base_cost > 0", name="check_base_cost_positive"),
        CheckConstraint("final_cost > 0", name="check_final_cost_positive")
    )


class AdditionalWork(Base):
    __tablename__ = 'additional_work_requests'      

    additional_work_requests_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    responded_by_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    description = Column(Text, nullable=False)
    additional_cost = Column(Numeric(precision=10, scale=2), nullable=False)
    additional_time_minutes = Column(Integer, nullable=True)
    status = Column(SQLEnum(AdditionalWorkRequestStatuses), nullable=False, index=True, default=AdditionalWorkRequestStatuses.PENDING)
    created_at = Column(DateTime, default=datetime.now(UTC))
    responded_at = Column(DateTime, nullable=True)
    order = relationship("Order", back_populates="additional_work_requests")
    responder = relationship("User", back_populates="additional_work_responses")
    
    __table_args__ = (
        CheckConstraint("additional_cost > 0", name="check_additional_cost_positive"),
    )
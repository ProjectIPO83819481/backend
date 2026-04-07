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
    email = Column(String(255), nullable=False, index=True)
    password_hash = Column(String(255), nullable=False, index=True)
    role = Column(SQLEnum(Role), nullable=False, index=True)
    full_name = Column(String(255), nullable=False, index=True)
    phone = Column(String(255), nullable=False, index=True)
    photo_url = Column(String(255), nullable=True, index=True)
    is_suspended = Column(Boolean, default=True, nullable=False)
    suspended_until = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    __tablename__ = 'orders'                       
    order_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, nullable = False)
    executor_id = Column(Integer, nullable = False)
    service_id = Column(Integer, nullable = False)
    status = role = Column(SQLEnum(Status), nullable=False, index=True)
    address = Column(String(255), nullable=True, index=True)
    scheduled_at = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, default=datetime.utcnow)
    cancelled_at = Column(DateTime, default=datetime.utcnow)
    cancelled_by_user_id = Column(Integer, nullable=False)
    cancellation_reason = Column(Text, nullable=True)
    review_comment = Column(Text, nullable=True)
    review_created_at = Column(DateTime, default=datetime.utcnow)
    review_executor_response = Column(String(255), nullable=True, index=True)
    base_cost = Column(Numeric(precision=10, scale=4), nullable=False)
    final_cost = Column(Numeric(precision=10, scale=4), nullable=False)
    __table_args__ = (
        CheckConstraint("base_cost > 0", name="check_base_cost_positive"),
        CheckConstraint("final_cost > 0", name="check_final_cost_positive")
    )


class AdditionalWork(Base):
    __tablename__ = 'additional_work_requests'      
    additional_work_requests_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable = False)
    description = Column(Text, nullable=True)
    additional_cost = Column(Numeric(precision=10, scale=4), nullable=False)
    additional_time_minutes = Column(Integer, nullable = True)
    status = Column(SQLEnum(AdditionalWorkRequestStatuses), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime, default=datetime.utcnow)
    responded_by_user_id = Column(Integer, nullable = False)
    __table_args__ = (
        CheckConstraint("additional_cost > 0", name="check_additional_cost_positive")
    
    )

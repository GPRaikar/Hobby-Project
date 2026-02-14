"""Transaction model."""
import uuid
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import Column, String, DateTime, Date, Boolean, Enum, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class TransactionType(str, enum.Enum):
    """Transaction type enumeration."""
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"
    TRANSFER = "TRANSFER"


class TransactionSource(str, enum.Enum):
    """Transaction source enumeration."""
    MANUAL = "MANUAL"
    SMS = "SMS"
    OCR = "OCR"
    BANK_SYNC = "BANK_SYNC"


class RecurringFrequency(str, enum.Enum):
    """Recurring frequency enumeration."""
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"


class RichDadCategory(str, enum.Enum):
    """Rich Dad category enumeration."""
    ACTIVE_INCOME = "ACTIVE_INCOME"
    PASSIVE_INCOME = "PASSIVE_INCOME"
    ASSET_EXPENSE = "ASSET_EXPENSE"
    LIABILITY_EXPENSE = "LIABILITY_EXPENSE"
    NECESSITY = "NECESSITY"


class Transaction(Base):
    """Transaction model for income and expenses."""
    
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(String, nullable=False)
    sub_category = Column(String, nullable=True)
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String, default="INR", nullable=False)
    description = Column(String, nullable=True)
    merchant_name = Column(String, nullable=True)
    source = Column(Enum(TransactionSource), default=TransactionSource.MANUAL, nullable=False)
    account_identifier = Column(String, nullable=True)  # Last 4 digits
    transaction_date = Column(Date, default=date.today, nullable=False)
    is_recurring = Column(Boolean, default=False, nullable=False)
    recurring_frequency = Column(Enum(RecurringFrequency), nullable=True)
    rich_dad_category = Column(Enum(RichDadCategory), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="transactions")

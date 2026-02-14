"""Transaction schemas."""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from app.models.transaction import (
    TransactionType,
    TransactionSource,
    RecurringFrequency,
    RichDadCategory
)


class TransactionBase(BaseModel):
    """Base transaction schema."""
    type: TransactionType
    category: str
    sub_category: Optional[str] = None
    amount: Decimal = Field(..., gt=0)
    currency: str = "INR"
    description: Optional[str] = None
    merchant_name: Optional[str] = None
    source: TransactionSource = TransactionSource.MANUAL
    account_identifier: Optional[str] = None
    transaction_date: date
    is_recurring: bool = False
    recurring_frequency: Optional[RecurringFrequency] = None
    rich_dad_category: Optional[RichDadCategory] = None


class TransactionCreate(TransactionBase):
    """Transaction creation schema."""
    pass


class TransactionUpdate(BaseModel):
    """Transaction update schema."""
    type: Optional[TransactionType] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    amount: Optional[Decimal] = Field(None, gt=0)
    currency: Optional[str] = None
    description: Optional[str] = None
    merchant_name: Optional[str] = None
    account_identifier: Optional[str] = None
    transaction_date: Optional[date] = None
    is_recurring: Optional[bool] = None
    recurring_frequency: Optional[RecurringFrequency] = None
    rich_dad_category: Optional[RichDadCategory] = None


class TransactionResponse(TransactionBase):
    """Transaction response schema."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

"""Budget schemas."""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class BudgetBase(BaseModel):
    """Base budget schema."""
    category: str
    monthly_limit: Decimal = Field(..., gt=0)
    financial_year: str


class BudgetCreate(BudgetBase):
    """Budget creation schema."""
    pass


class BudgetUpdate(BaseModel):
    """Budget update schema."""
    category: Optional[str] = None
    monthly_limit: Optional[Decimal] = Field(None, gt=0)
    financial_year: Optional[str] = None


class BudgetResponse(BudgetBase):
    """Budget response schema."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BudgetWithSpending(BudgetResponse):
    """Budget response with spending information."""
    spent: Decimal
    remaining: Decimal
    percentage_used: float

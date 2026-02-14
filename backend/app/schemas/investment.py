"""Investment schemas."""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from app.models.investment import InvestmentType, TaxSection, AssetLiabilityCategory


class InvestmentBase(BaseModel):
    """Base investment schema."""
    name: str
    investment_type: InvestmentType
    amount_invested: Decimal = Field(..., gt=0)
    current_value: Optional[Decimal] = None
    annual_return_pct: Optional[Decimal] = None
    start_date: date
    maturity_date: Optional[date] = None
    is_tax_saving: bool = False
    tax_section: TaxSection = TaxSection.NONE
    folio_number: Optional[str] = None
    ticker_symbol: Optional[str] = None
    is_active: bool = True
    rich_dad_category: AssetLiabilityCategory = AssetLiabilityCategory.ASSET
    passive_income_amount: Decimal = Field(default=0, ge=0)


class InvestmentCreate(InvestmentBase):
    """Investment creation schema."""
    pass


class InvestmentUpdate(BaseModel):
    """Investment update schema."""
    name: Optional[str] = None
    investment_type: Optional[InvestmentType] = None
    amount_invested: Optional[Decimal] = Field(None, gt=0)
    current_value: Optional[Decimal] = None
    annual_return_pct: Optional[Decimal] = None
    start_date: Optional[date] = None
    maturity_date: Optional[date] = None
    is_tax_saving: Optional[bool] = None
    tax_section: Optional[TaxSection] = None
    folio_number: Optional[str] = None
    ticker_symbol: Optional[str] = None
    is_active: Optional[bool] = None
    rich_dad_category: Optional[AssetLiabilityCategory] = None
    passive_income_amount: Optional[Decimal] = Field(None, ge=0)


class InvestmentResponse(InvestmentBase):
    """Investment response schema."""
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

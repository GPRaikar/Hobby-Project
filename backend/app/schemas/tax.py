"""Tax schemas."""
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel
from app.models.tax_deduction import TaxDeductionSection


class Section80CResponse(BaseModel):
    """Section 80C calculation response."""
    total_invested: Decimal
    utilized: Decimal
    remaining: Decimal
    percentage_used: float
    tax_saved: Decimal
    limit: Decimal = Decimal("150000")


class Section80DResponse(BaseModel):
    """Section 80D calculation response."""
    individual_invested: Decimal
    individual_limit: Decimal
    parents_invested: Decimal
    parents_limit: Decimal
    total_utilized: Decimal
    total_limit: Decimal
    remaining: Decimal
    tax_saved: Decimal


class TaxSlabBreakdown(BaseModel):
    """Tax slab breakdown."""
    slab_start: Decimal
    slab_end: Optional[Decimal]
    rate: Decimal
    taxable_in_slab: Decimal
    tax_amount: Decimal


class TaxCalculationResponse(BaseModel):
    """Tax calculation response."""
    gross_income: Decimal
    standard_deduction: Decimal
    total_deductions: Decimal
    taxable_income: Decimal
    tax_before_rebate: Decimal
    rebate_87a: Decimal
    total_tax: Decimal
    cess: Decimal
    final_tax: Decimal
    slabs: List[TaxSlabBreakdown]
    regime: str  # "NEW" or "OLD"


class TaxComparisonResponse(BaseModel):
    """Tax regime comparison response."""
    new_regime: TaxCalculationResponse
    old_regime: TaxCalculationResponse
    recommended_regime: str
    savings_with_recommended: Decimal


class TaxSummaryRequest(BaseModel):
    """Tax summary request."""
    financial_year: str
    gross_income: Decimal
    regime: str = "NEW"  # "NEW" or "OLD"

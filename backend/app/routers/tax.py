"""Tax router for tax calculations and planning."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from decimal import Decimal
from app.database import get_db
from app.models.user import User
from app.schemas.tax import (
    Section80CResponse,
    Section80DResponse,
    TaxCalculationResponse,
    TaxComparisonResponse,
    TaxSummaryRequest,
)
from app.services.tax_calculator import (
    calculate_80c,
    calculate_80d,
    calculate_tax_new_regime,
    calculate_tax_old_regime,
    compare_tax_regimes,
)
from app.utils.dependencies import get_current_user
from app.utils.constants import NEW_REGIME_STANDARD_DEDUCTION

router = APIRouter(prefix="/tax", tags=["Tax Planning"])


@router.get("/section-80c", response_model=Section80CResponse)
def get_section_80c(
    financial_year: str = "2025-26",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get Section 80C utilization and tax savings."""
    return calculate_80c(db, str(current_user.id), financial_year)


@router.get("/section-80d", response_model=Section80DResponse)
def get_section_80d(
    financial_year: str = "2025-26",
    is_senior: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get Section 80D utilization and tax savings."""
    return calculate_80d(db, str(current_user.id), financial_year, is_senior)


@router.post("/calculate", response_model=TaxCalculationResponse)
def calculate_tax(
    tax_request: TaxSummaryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Calculate tax for given gross income and regime."""
    if tax_request.regime.upper() == "NEW":
        return calculate_tax_new_regime(tax_request.gross_income, NEW_REGIME_STANDARD_DEDUCTION)
    else:
        # For old regime, get deductions
        section_80c = calculate_80c(db, str(current_user.id), tax_request.financial_year)
        return calculate_tax_old_regime(tax_request.gross_income, section_80c.utilized)


@router.get("/compare", response_model=TaxComparisonResponse)
def compare_regimes(
    gross_income: Decimal,
    financial_year: str = "2025-26",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compare tax under new and old regimes."""
    return compare_tax_regimes(db, str(current_user.id), gross_income, financial_year)

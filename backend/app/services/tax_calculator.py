"""Tax calculator service for Indian tax calculations."""
from decimal import Decimal
from typing import List, Tuple
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.investment import Investment
from app.models.transaction import Transaction, TransactionType
from app.utils.constants import (
    TAX_80C_LIMIT,
    TAX_80CCD_1B_LIMIT,
    TAX_80D_INDIVIDUAL_LIMIT,
    TAX_80D_SENIOR_CITIZEN_LIMIT,
    NEW_TAX_REGIME_SLABS,
    NEW_REGIME_STANDARD_DEDUCTION,
    NEW_REGIME_REBATE_LIMIT,
    OLD_TAX_REGIME_SLABS,
    OLD_REGIME_REBATE_LIMIT,
)
from app.schemas.tax import (
    Section80CResponse,
    Section80DResponse,
    TaxSlabBreakdown,
    TaxCalculationResponse,
    TaxComparisonResponse,
)


def calculate_80c(db: Session, user_id: str, financial_year: str) -> Section80CResponse:
    """Calculate Section 80C utilization and savings."""
    # Query investments marked as 80C
    investments = db.query(Investment).filter(
        Investment.user_id == user_id,
        Investment.tax_section == "80C",
        Investment.is_active == True
    ).all()
    
    total_invested = sum(inv.amount_invested for inv in investments)
    utilized = min(total_invested, TAX_80C_LIMIT)
    remaining = TAX_80C_LIMIT - utilized
    percentage_used = float((utilized / TAX_80C_LIMIT) * 100)
    
    # Assuming 30% tax bracket for calculation
    tax_saved = utilized * Decimal("0.30")
    
    return Section80CResponse(
        total_invested=total_invested,
        utilized=utilized,
        remaining=remaining,
        percentage_used=percentage_used,
        tax_saved=tax_saved,
        limit=TAX_80C_LIMIT
    )


def calculate_80d(db: Session, user_id: str, financial_year: str, is_senior: bool = False) -> Section80DResponse:
    """Calculate Section 80D utilization and savings."""
    # Query investments marked as 80D
    investments = db.query(Investment).filter(
        Investment.user_id == user_id,
        Investment.tax_section == "80D",
        Investment.is_active == True
    ).all()
    
    individual_limit = TAX_80D_SENIOR_CITIZEN_LIMIT if is_senior else TAX_80D_INDIVIDUAL_LIMIT
    parents_limit = TAX_80D_SENIOR_CITIZEN_LIMIT  # Assuming parents are senior
    
    # For simplicity, split investments equally between individual and parents
    total_invested = sum(inv.amount_invested for inv in investments)
    individual_invested = total_invested / 2
    parents_invested = total_invested / 2
    
    individual_utilized = min(individual_invested, individual_limit)
    parents_utilized = min(parents_invested, parents_limit)
    total_utilized = individual_utilized + parents_utilized
    total_limit = individual_limit + parents_limit
    remaining = total_limit - total_utilized
    
    # Assuming 30% tax bracket
    tax_saved = total_utilized * Decimal("0.30")
    
    return Section80DResponse(
        individual_invested=individual_invested,
        individual_limit=individual_limit,
        parents_invested=parents_invested,
        parents_limit=parents_limit,
        total_utilized=total_utilized,
        total_limit=total_limit,
        remaining=remaining,
        tax_saved=tax_saved
    )


def calculate_tax_new_regime(gross_income: Decimal, standard_deduction: Decimal) -> TaxCalculationResponse:
    """Calculate tax under new regime."""
    taxable_income = gross_income - standard_deduction
    
    slabs: List[TaxSlabBreakdown] = []
    tax_before_rebate = Decimal("0")
    previous_limit = Decimal("0")
    
    for limit, rate in NEW_TAX_REGIME_SLABS:
        if taxable_income <= previous_limit:
            break
        
        slab_end = Decimal(str(limit)) if limit != float("inf") else None
        taxable_in_slab = min(taxable_income, Decimal(str(limit)) if limit != float("inf") else taxable_income) - previous_limit
        
        if taxable_in_slab > 0:
            tax_amount = taxable_in_slab * rate
            tax_before_rebate += tax_amount
            
            slabs.append(TaxSlabBreakdown(
                slab_start=previous_limit,
                slab_end=slab_end,
                rate=rate,
                taxable_in_slab=taxable_in_slab,
                tax_amount=tax_amount
            ))
        
        previous_limit = Decimal(str(limit)) if limit != float("inf") else previous_limit
    
    # Apply rebate under 87A
    rebate_87a = Decimal("0")
    if taxable_income <= NEW_REGIME_REBATE_LIMIT:
        rebate_87a = tax_before_rebate
    
    total_tax = tax_before_rebate - rebate_87a
    cess = total_tax * Decimal("0.04")  # 4% cess
    final_tax = total_tax + cess
    
    return TaxCalculationResponse(
        gross_income=gross_income,
        standard_deduction=standard_deduction,
        total_deductions=standard_deduction,
        taxable_income=taxable_income,
        tax_before_rebate=tax_before_rebate,
        rebate_87a=rebate_87a,
        total_tax=total_tax,
        cess=cess,
        final_tax=final_tax,
        slabs=slabs,
        regime="NEW"
    )


def calculate_tax_old_regime(gross_income: Decimal, deductions: Decimal) -> TaxCalculationResponse:
    """Calculate tax under old regime."""
    taxable_income = gross_income - deductions
    
    slabs: List[TaxSlabBreakdown] = []
    tax_before_rebate = Decimal("0")
    previous_limit = Decimal("0")
    
    for limit, rate in OLD_TAX_REGIME_SLABS:
        if taxable_income <= previous_limit:
            break
        
        slab_end = Decimal(str(limit)) if limit != float("inf") else None
        taxable_in_slab = min(taxable_income, Decimal(str(limit)) if limit != float("inf") else taxable_income) - previous_limit
        
        if taxable_in_slab > 0:
            tax_amount = taxable_in_slab * rate
            tax_before_rebate += tax_amount
            
            slabs.append(TaxSlabBreakdown(
                slab_start=previous_limit,
                slab_end=slab_end,
                rate=rate,
                taxable_in_slab=taxable_in_slab,
                tax_amount=tax_amount
            ))
        
        previous_limit = Decimal(str(limit)) if limit != float("inf") else previous_limit
    
    # Apply rebate under 87A
    rebate_87a = Decimal("0")
    if taxable_income <= OLD_REGIME_REBATE_LIMIT:
        rebate_87a = tax_before_rebate
    
    total_tax = tax_before_rebate - rebate_87a
    cess = total_tax * Decimal("0.04")  # 4% cess
    final_tax = total_tax + cess
    
    return TaxCalculationResponse(
        gross_income=gross_income,
        standard_deduction=Decimal("0"),
        total_deductions=deductions,
        taxable_income=taxable_income,
        tax_before_rebate=tax_before_rebate,
        rebate_87a=rebate_87a,
        total_tax=total_tax,
        cess=cess,
        final_tax=final_tax,
        slabs=slabs,
        regime="OLD"
    )


def compare_tax_regimes(db: Session, user_id: str, gross_income: Decimal, financial_year: str) -> TaxComparisonResponse:
    """Compare tax under new and old regimes."""
    # Calculate 80C for old regime
    section_80c = calculate_80c(db, user_id, financial_year)
    total_deductions = section_80c.utilized
    
    # Calculate tax under both regimes
    new_regime_tax = calculate_tax_new_regime(gross_income, NEW_REGIME_STANDARD_DEDUCTION)
    old_regime_tax = calculate_tax_old_regime(gross_income, total_deductions)
    
    # Determine recommended regime
    if new_regime_tax.final_tax < old_regime_tax.final_tax:
        recommended_regime = "NEW"
        savings = old_regime_tax.final_tax - new_regime_tax.final_tax
    else:
        recommended_regime = "OLD"
        savings = new_regime_tax.final_tax - old_regime_tax.final_tax
    
    return TaxComparisonResponse(
        new_regime=new_regime_tax,
        old_regime=old_regime_tax,
        recommended_regime=recommended_regime,
        savings_with_recommended=savings
    )

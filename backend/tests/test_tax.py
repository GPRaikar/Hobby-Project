"""Test tax calculation service."""
import pytest
from decimal import Decimal
from app.services.tax_calculator import calculate_tax_new_regime, calculate_tax_old_regime
from app.utils.constants import NEW_REGIME_STANDARD_DEDUCTION


def test_tax_new_regime_below_exemption():
    """Test new regime tax calculation for income below exemption limit."""
    result = calculate_tax_new_regime(Decimal("300000"), NEW_REGIME_STANDARD_DEDUCTION)
    
    assert result.taxable_income == Decimal("225000")
    assert result.final_tax == Decimal("0")
    assert result.regime == "NEW"


def test_tax_new_regime_middle_bracket():
    """Test new regime tax calculation for middle income bracket."""
    result = calculate_tax_new_regime(Decimal("800000"), NEW_REGIME_STANDARD_DEDUCTION)
    
    assert result.taxable_income == Decimal("725000")
    assert result.regime == "NEW"
    assert result.final_tax > Decimal("0")


def test_tax_new_regime_with_rebate():
    """Test new regime with 87A rebate."""
    result = calculate_tax_new_regime(Decimal("700000"), NEW_REGIME_STANDARD_DEDUCTION)
    
    # Income is within rebate limit, so final tax should be 0
    assert result.taxable_income == Decimal("625000")
    assert result.rebate_87a == result.tax_before_rebate
    assert result.total_tax == Decimal("0")


def test_tax_old_regime():
    """Test old regime tax calculation."""
    result = calculate_tax_old_regime(Decimal("800000"), Decimal("150000"))
    
    assert result.taxable_income == Decimal("650000")
    assert result.regime == "OLD"
    assert result.final_tax > Decimal("0")


def test_tax_old_regime_with_deductions():
    """Test old regime with maximum deductions."""
    result = calculate_tax_old_regime(Decimal("1000000"), Decimal("150000"))
    
    assert result.total_deductions == Decimal("150000")
    assert result.taxable_income == Decimal("850000")

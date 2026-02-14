"""Test SMS parser service."""
import pytest
from decimal import Decimal
from app.services.sms_parser import parse_sms


def test_parse_hdfc_debit_sms():
    """Test parsing HDFC Bank debit SMS."""
    sms = "Rs.1,500.00 debited from a/c **1234 on 14-02-26 to VPA merchant@upi (UPI Ref No 123456789). Avl Bal Rs.50,000.00"
    result = parse_sms(sms)
    
    assert result.success is True
    assert result.bank == "HDFC"
    assert result.amount == Decimal("1500.00")
    assert result.transaction_type == "DEBIT"
    assert result.account_last4 == "1234"
    assert result.available_balance == Decimal("50000.00")


def test_parse_sbi_sms():
    """Test parsing SBI Bank SMS."""
    sms = "Your a/c no. XX1234 is debited by Rs.500.00 on 14Feb26 (UPI Ref No 123456). If not done by u, call..."
    result = parse_sms(sms)
    
    assert result.success is True
    assert result.bank == "SBI"
    assert result.amount == Decimal("500.00")
    assert result.transaction_type == "DEBIT"
    assert result.account_last4 == "1234"


def test_parse_icici_sms():
    """Test parsing ICICI Bank SMS."""
    sms = "ICICI Bank Acct XX1234 debited for Rs 2,500.00 on 14-Feb-26; UPI:merchant@bank credited. UPI Ref:123456"
    result = parse_sms(sms)
    
    assert result.success is True
    assert result.bank == "ICICI"
    assert result.amount == Decimal("2500.00")
    assert result.transaction_type == "DEBIT"
    assert result.account_last4 == "1234"


def test_parse_credit_card_sms():
    """Test parsing credit card SMS."""
    sms = "Your HDFC Credit Card XX1234 has been used for a transaction of INR 5,000.00 at MERCHANT on 14-02-2026"
    result = parse_sms(sms)
    
    assert result.success is True
    assert result.bank == "CREDIT_CARD"
    assert result.amount == Decimal("5000.00")
    assert result.transaction_type == "DEBIT"
    assert result.account_last4 == "1234"


def test_parse_invalid_sms():
    """Test parsing invalid SMS."""
    sms = "This is not a bank SMS message"
    result = parse_sms(sms)
    
    assert result.success is False
    assert result.amount is None

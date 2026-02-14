"""SMS parser service for Indian bank SMS patterns."""
import re
from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional, List
from app.utils.constants import SMS_PATTERNS


class SMSParseResult:
    """SMS parse result container."""
    
    def __init__(
        self,
        amount: Optional[Decimal] = None,
        transaction_type: Optional[str] = None,
        account_last4: Optional[str] = None,
        merchant: Optional[str] = None,
        date: Optional[str] = None,
        reference_number: Optional[str] = None,
        available_balance: Optional[Decimal] = None,
        raw_sms: str = "",
        bank: Optional[str] = None,
        success: bool = False
    ):
        self.amount = amount
        self.transaction_type = transaction_type
        self.account_last4 = account_last4
        self.merchant = merchant
        self.date = date
        self.reference_number = reference_number
        self.available_balance = available_balance
        self.raw_sms = raw_sms
        self.bank = bank
        self.success = success
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "amount": str(self.amount) if self.amount else None,
            "transaction_type": self.transaction_type,
            "account_last4": self.account_last4,
            "merchant": self.merchant,
            "date": self.date,
            "reference_number": self.reference_number,
            "available_balance": str(self.available_balance) if self.available_balance else None,
            "raw_sms": self.raw_sms,
            "bank": self.bank,
            "success": self.success
        }


def clean_amount(amount_str: str) -> Decimal:
    """Clean and convert amount string to Decimal."""
    # Remove commas and convert to Decimal
    cleaned = amount_str.replace(",", "")
    return Decimal(cleaned)


def parse_sms(sms_text: str) -> SMSParseResult:
    """Parse SMS text and extract transaction details."""
    result = SMSParseResult(raw_sms=sms_text)
    
    # Try each bank pattern
    for bank, pattern in SMS_PATTERNS.items():
        match = re.search(pattern, sms_text, re.IGNORECASE)
        if match:
            result.bank = bank
            result.success = True
            
            if bank == "HDFC":
                result.amount = clean_amount(match.group(1))
                result.transaction_type = "DEBIT" if "debited" in match.group(2).lower() else "CREDIT"
                result.account_last4 = match.group(3)
                result.date = match.group(4)
                result.merchant = match.group(5) if match.group(5) is not None else None
                result.reference_number = match.group(6) if match.group(6) is not None else None
                result.available_balance = clean_amount(match.group(7)) if match.group(7) is not None else None
            
            elif bank == "SBI":
                result.account_last4 = match.group(1)
                result.transaction_type = "DEBIT" if "debited" in match.group(2).lower() else "CREDIT"
                result.amount = clean_amount(match.group(3))
                result.date = match.group(4)
                result.reference_number = match.group(5) if match.group(5) is not None else None
            
            elif bank == "ICICI":
                result.account_last4 = match.group(1)
                result.transaction_type = "DEBIT" if "debited" in match.group(2).lower() else "CREDIT"
                result.amount = clean_amount(match.group(3))
                result.date = match.group(4)
                result.merchant = match.group(5) if match.group(5) is not None else None
                result.reference_number = match.group(6) if match.group(6) is not None else None
            
            elif bank == "AXIS":
                result.amount = clean_amount(match.group(1))
                result.account_last4 = match.group(2)
                result.merchant = match.group(3) if match.group(3) is not None else None
                result.date = match.group(4)
                result.reference_number = match.group(5)
                result.transaction_type = "DEBIT"  # Axis pattern is for sent money
            
            elif bank == "KOTAK":
                result.amount = clean_amount(match.group(1))
                result.transaction_type = "DEBIT" if "debited" in match.group(2).lower() else "CREDIT"
                result.account_last4 = match.group(3)
                result.date = match.group(4)
                result.merchant = match.group(5) if match.group(5) is not None else None
                result.available_balance = clean_amount(match.group(6)) if match.group(6) is not None else None
            
            elif bank == "CREDIT_CARD":
                result.account_last4 = match.group(1)
                result.amount = clean_amount(match.group(2))
                result.merchant = match.group(3)
                result.date = match.group(4)
                result.transaction_type = "DEBIT"  # Credit card usage is debit
            
            break
    
    return result


def parse_multiple_sms(sms_list: List[str]) -> List[SMSParseResult]:
    """Parse multiple SMS messages."""
    results = []
    for sms in sms_list:
        result = parse_sms(sms)
        if result.success:
            results.append(result)
    return results

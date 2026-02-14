"""Constants for the application."""
from decimal import Decimal

# Tax limits (FY 2025-26)
TAX_80C_LIMIT = Decimal("150000")
TAX_80CCD_1B_LIMIT = Decimal("50000")
TAX_80D_INDIVIDUAL_LIMIT = Decimal("25000")
TAX_80D_SENIOR_CITIZEN_LIMIT = Decimal("50000")
TAX_80D_PREVENTIVE_LIMIT = Decimal("5000")

# New Tax Regime Slabs (FY 2025-26)
NEW_TAX_REGIME_SLABS = [
    (Decimal("300000"), Decimal("0")),
    (Decimal("700000"), Decimal("0.05")),
    (Decimal("1000000"), Decimal("0.10")),
    (Decimal("1200000"), Decimal("0.15")),
    (Decimal("1500000"), Decimal("0.20")),
    (float("inf"), Decimal("0.30")),
]

NEW_REGIME_STANDARD_DEDUCTION = Decimal("75000")
NEW_REGIME_REBATE_LIMIT = Decimal("700000")

# Old Tax Regime Slabs
OLD_TAX_REGIME_SLABS = [
    (Decimal("250000"), Decimal("0")),
    (Decimal("500000"), Decimal("0.05")),
    (Decimal("1000000"), Decimal("0.20")),
    (float("inf"), Decimal("0.30")),
]

OLD_REGIME_REBATE_LIMIT = Decimal("500000")

# SMS Parser Regex Patterns for Indian Banks
SMS_PATTERNS = {
    "HDFC": r"Rs\.([0-9,]+\.\d{2})\s+(debited|credited).*?a/c\s+\*\*(\d{4}).*?on\s+(\d{2}-\d{2}-\d{2}).*?(?:to\s+(.+?))?\s*(?:\(UPI Ref No\s+(\d+)\))?.*?Avl Bal Rs\.([0-9,]+\.\d{2})",
    "SBI": r"Your a/c no\.\s+XX(\d{4}).*?(debited|credited).*?Rs\.([0-9,]+\.\d{2}).*?on\s+(\d{2}\w{3}\d{2}).*?(?:UPI Ref No\s+(\d+))?",
    "ICICI": r"ICICI Bank Acct XX(\d{4})\s+(debited|credited).*?Rs\s+([0-9,]+\.\d{2}).*?on\s+(\d{2}-\w{3}-\d{2}).*?(?:UPI:(.+?))?\s*(?:UPI Ref:(\d+))?",
    "AXIS": r"Rs\.([0-9,]+\.\d{2}).*?(?:sent from|credited to).*?Axis Bank A/C no\.\s+XX(\d{4}).*?(?:to\s+(.+?))?\s*via UPI on\s+(\d{2}-\d{2}-\d{4}).*?UPI Ref no:\s+(\d+)",
    "KOTAK": r"Amt of Rs\.([0-9,]+\.\d{2})\s+(debited|credited).*?A/c XX(\d{4}).*?on\s+(\d{2}-\d{2}-\d{2}).*?(?:towards\s+(.+?))?\.\s*Avl Bal:\s+Rs\.([0-9,]+\.\d{2})",
    "CREDIT_CARD": r"Credit Card XX(\d{4}).*?transaction of INR\s+([0-9,]+\.\d{2}).*?at\s+(.+?)\s+on\s+(\d{2}-\d{2}-\d{4})",
}

# Default categories
INCOME_CATEGORIES = ["Salary", "Freelance", "Business", "Investment Returns", "Rental Income", "Dividends", "Interest", "Other"]
EXPENSE_CATEGORIES = ["Rent", "Groceries", "Transportation", "Utilities", "Healthcare", "Entertainment", "Shopping", "Food", "Education", "Insurance", "Investment", "EMI", "Other"]

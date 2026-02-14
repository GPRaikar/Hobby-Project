"""Dashboard schemas."""
from decimal import Decimal
from datetime import date
from typing import List
from pydantic import BaseModel


class IncomeExpenseSummary(BaseModel):
    """Income and expense summary."""
    total_income: Decimal
    active_income: Decimal
    passive_income: Decimal
    total_expenses: Decimal
    asset_expenses: Decimal
    liability_expenses: Decimal
    necessity_expenses: Decimal


class AssetLiabilitySummary(BaseModel):
    """Assets and liabilities summary."""
    total_assets_value: Decimal
    total_liabilities_value: Decimal
    net_worth: Decimal
    asset_count: int
    liability_count: int


class MonthlyTrend(BaseModel):
    """Monthly trend data."""
    month: str
    income: Decimal
    expenses: Decimal
    savings: Decimal


class RichDadDashboard(BaseModel):
    """Rich Dad Dashboard response."""
    income_expense_summary: IncomeExpenseSummary
    asset_liability_summary: AssetLiabilitySummary
    financial_freedom_ratio: float
    cash_flow: Decimal
    savings_rate: float
    passive_income_goal_percentage: float
    monthly_trends: List[MonthlyTrend]
    period_start: date
    period_end: date

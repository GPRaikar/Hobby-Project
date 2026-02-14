"""Dashboard service for Rich Dad calculations."""
from decimal import Decimal
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List
from app.models.transaction import Transaction, TransactionType, RichDadCategory
from app.models.investment import Investment, AssetLiabilityCategory
from app.schemas.dashboard import (
    IncomeExpenseSummary,
    AssetLiabilitySummary,
    MonthlyTrend,
    RichDadDashboard,
)


def calculate_income_expense_summary(db: Session, user_id: str, start_date: date, end_date: date) -> IncomeExpenseSummary:
    """Calculate income and expense summary."""
    # Get all transactions in the period
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_date >= start_date,
        Transaction.transaction_date <= end_date
    ).all()
    
    total_income = Decimal("0")
    active_income = Decimal("0")
    passive_income = Decimal("0")
    total_expenses = Decimal("0")
    asset_expenses = Decimal("0")
    liability_expenses = Decimal("0")
    necessity_expenses = Decimal("0")
    
    for txn in transactions:
        if txn.type == TransactionType.INCOME:
            total_income += txn.amount
            if txn.rich_dad_category == RichDadCategory.ACTIVE_INCOME:
                active_income += txn.amount
            elif txn.rich_dad_category == RichDadCategory.PASSIVE_INCOME:
                passive_income += txn.amount
        elif txn.type == TransactionType.EXPENSE:
            total_expenses += txn.amount
            if txn.rich_dad_category == RichDadCategory.ASSET_EXPENSE:
                asset_expenses += txn.amount
            elif txn.rich_dad_category == RichDadCategory.LIABILITY_EXPENSE:
                liability_expenses += txn.amount
            elif txn.rich_dad_category == RichDadCategory.NECESSITY:
                necessity_expenses += txn.amount
    
    return IncomeExpenseSummary(
        total_income=total_income,
        active_income=active_income,
        passive_income=passive_income,
        total_expenses=total_expenses,
        asset_expenses=asset_expenses,
        liability_expenses=liability_expenses,
        necessity_expenses=necessity_expenses
    )


def calculate_asset_liability_summary(db: Session, user_id: str) -> AssetLiabilitySummary:
    """Calculate assets and liabilities summary."""
    # Get all active investments
    investments = db.query(Investment).filter(
        Investment.user_id == user_id,
        Investment.is_active == True
    ).all()
    
    total_assets_value = Decimal("0")
    total_liabilities_value = Decimal("0")
    asset_count = 0
    liability_count = 0
    
    for inv in investments:
        value = inv.current_value if inv.current_value else inv.amount_invested
        if inv.rich_dad_category == AssetLiabilityCategory.ASSET:
            total_assets_value += value
            asset_count += 1
        elif inv.rich_dad_category == AssetLiabilityCategory.LIABILITY:
            total_liabilities_value += value
            liability_count += 1
    
    net_worth = total_assets_value - total_liabilities_value
    
    return AssetLiabilitySummary(
        total_assets_value=total_assets_value,
        total_liabilities_value=total_liabilities_value,
        net_worth=net_worth,
        asset_count=asset_count,
        liability_count=liability_count
    )


def calculate_monthly_trends(db: Session, user_id: str, months: int = 6) -> List[MonthlyTrend]:
    """Calculate monthly trends for the past N months."""
    trends = []
    end_date = date.today()
    
    for i in range(months):
        month_start = (end_date - relativedelta(months=i)).replace(day=1)
        if i == 0:
            month_end = end_date
        else:
            month_end = month_start + relativedelta(months=1) - relativedelta(days=1)
        
        # Calculate income and expenses for this month
        transactions = db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= month_start,
            Transaction.transaction_date <= month_end
        ).all()
        
        income = sum(txn.amount for txn in transactions if txn.type == TransactionType.INCOME)
        expenses = sum(txn.amount for txn in transactions if txn.type == TransactionType.EXPENSE)
        savings = income - expenses
        
        trends.insert(0, MonthlyTrend(
            month=month_start.strftime("%b %Y"),
            income=income,
            expenses=expenses,
            savings=savings
        ))
    
    return trends


def get_rich_dad_dashboard(db: Session, user_id: str, months: int = 6) -> RichDadDashboard:
    """Get complete Rich Dad Dashboard data."""
    end_date = date.today()
    start_date = end_date - relativedelta(months=months)
    
    # Calculate summaries
    income_expense_summary = calculate_income_expense_summary(db, user_id, start_date, end_date)
    asset_liability_summary = calculate_asset_liability_summary(db, user_id)
    monthly_trends = calculate_monthly_trends(db, user_id, months)
    
    # Calculate financial freedom ratio
    # Financial Freedom Ratio = (Passive Income / Total Expenses) × 100
    if income_expense_summary.total_expenses > 0:
        financial_freedom_ratio = float(
            (income_expense_summary.passive_income / income_expense_summary.total_expenses) * 100
        )
    else:
        financial_freedom_ratio = 0.0
    
    # Calculate cash flow
    cash_flow = income_expense_summary.total_income - income_expense_summary.total_expenses
    
    # Calculate savings rate
    if income_expense_summary.total_income > 0:
        savings_rate = float(
            (cash_flow / income_expense_summary.total_income) * 100
        )
    else:
        savings_rate = 0.0
    
    # Calculate passive income goal percentage (goal is 100%)
    passive_income_goal_percentage = min(financial_freedom_ratio, 100.0)
    
    return RichDadDashboard(
        income_expense_summary=income_expense_summary,
        asset_liability_summary=asset_liability_summary,
        financial_freedom_ratio=financial_freedom_ratio,
        cash_flow=cash_flow,
        savings_rate=savings_rate,
        passive_income_goal_percentage=passive_income_goal_percentage,
        monthly_trends=monthly_trends,
        period_start=start_date,
        period_end=end_date
    )

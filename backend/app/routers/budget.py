"""Budget router for budget management."""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal
from datetime import date
from dateutil.relativedelta import relativedelta
from app.database import get_db
from app.models.user import User
from app.models.budget import Budget
from app.models.transaction import Transaction, TransactionType
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse, BudgetWithSpending
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.post("/", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
def create_budget(
    budget_data: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new budget."""
    new_budget = Budget(
        user_id=current_user.id,
        **budget_data.dict()
    )
    
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    
    return new_budget


@router.get("/", response_model=List[BudgetWithSpending])
def get_budgets(
    financial_year: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all budgets for the current user with spending information."""
    query = db.query(Budget).filter(Budget.user_id == current_user.id)
    
    if financial_year:
        query = query.filter(Budget.financial_year == financial_year)
    
    budgets = query.all()
    
    # Calculate spending for each budget
    result = []
    current_month_start = date.today().replace(day=1)
    current_month_end = (current_month_start + relativedelta(months=1)) - relativedelta(days=1)
    
    for budget in budgets:
        # Get expenses for this category in current month
        spent = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == current_user.id,
            Transaction.type == TransactionType.EXPENSE,
            Transaction.category == budget.category,
            Transaction.transaction_date >= current_month_start,
            Transaction.transaction_date <= current_month_end
        ).scalar() or Decimal("0")
        
        remaining = budget.monthly_limit - spent
        percentage_used = float((spent / budget.monthly_limit) * 100) if budget.monthly_limit > 0 else 0
        
        result.append(BudgetWithSpending(
            **budget.__dict__,
            spent=spent,
            remaining=remaining,
            percentage_used=percentage_used
        ))
    
    return result


@router.get("/{budget_id}", response_model=BudgetResponse)
def get_budget(
    budget_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific budget."""
    budget = db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == current_user.id
    ).first()
    
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    
    return budget


@router.put("/{budget_id}", response_model=BudgetResponse)
def update_budget(
    budget_id: UUID,
    budget_data: BudgetUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a budget."""
    budget = db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == current_user.id
    ).first()
    
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    
    # Update fields
    update_data = budget_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(budget, field, value)
    
    db.commit()
    db.refresh(budget)
    
    return budget


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(
    budget_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a budget."""
    budget = db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == current_user.id
    ).first()
    
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    
    db.delete(budget)
    db.commit()
    
    return None

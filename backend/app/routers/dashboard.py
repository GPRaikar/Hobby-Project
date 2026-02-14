"""Dashboard router for Rich Dad dashboard data."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.dashboard import RichDadDashboard
from app.services.dashboard_service import get_rich_dad_dashboard
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/", response_model=RichDadDashboard)
def get_dashboard(
    months: int = 6,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get Rich Dad Dashboard data."""
    return get_rich_dad_dashboard(db, str(current_user.id), months)

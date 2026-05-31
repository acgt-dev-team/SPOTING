from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.services.dashboard_service import (
    get_dashboard_stats,
    get_organization_performance
)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# =========================
# BASIC STATS (for cards)
# =========================
@router.get("/")
def dashboard(db: Session = Depends(get_db)):
    return get_dashboard_stats(db)


# =========================
# FULL DASHBOARD (stats + table)
# =========================
@router.get("/full")
def dashboard_full(db: Session = Depends(get_db)):
    return {
        "stats": get_dashboard_stats(db),
        "organizations": get_organization_performance(db)
    }
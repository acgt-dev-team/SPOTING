from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.report_service import generate_report

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)

@router.post("/profil/{profil_id}")
def generate(profil_id: int, db: Session = Depends(get_db)):
    return generate_report(db, profil_id)
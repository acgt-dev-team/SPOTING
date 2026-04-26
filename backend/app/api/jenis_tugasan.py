from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.services.jenis_tugasan_service import get_all_jenis

router = APIRouter(prefix="/jenis_tugasan", tags=["Jenis Tugasan"])


@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return get_all_jenis(db)
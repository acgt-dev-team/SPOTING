from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.schemas.tugasan_schema import TugasanCreate, TugasanResponse

from app.services.tugasan_service import (
    get_tugasan_by_profil,
    assign_tugasan_to_profil,
    get_all_tugasan
)

router = APIRouter(prefix="/tugasan", tags=["Tugasan"])


@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return get_all_tugasan(db)


@router.get("/profil/{profil_id}")
def get_by_profil(profil_id: int, db: Session = Depends(get_db)):
    return get_tugasan_by_profil(db, profil_id)


@router.post("/", response_model=TugasanResponse)
def create(data: TugasanCreate, db: Session = Depends(get_db)):
    return create_tugasan(db, data.dict())
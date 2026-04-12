from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.schemas.tugasan_schema import TugasanCreate, TugasanResponse

from app.services.tugasan_service import (
    get_tugasan_by_profil,
    assign_tugasan_to_profil,
    remove_tugasan_from_profil,
    get_all_tugasan,
)

router = APIRouter(prefix="/tugasan", tags=["Tugasan"])


# ✅ GET ALL (for dropdown)
@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return get_all_tugasan(db)


# ✅ GET ASSIGNED
@router.get("/profil/{profil_id}")
def get_by_profil(profil_id: int, db: Session = Depends(get_db)):
    return get_tugasan_by_profil(db, profil_id)


# ✅ ASSIGN
@router.post("/profil/{profil_id}")
def assign(profil_id: int, data: dict, db: Session = Depends(get_db)):
    return assign_tugasan_to_profil(
        db,
        profil_id=profil_id,
        tugasan_id=data["tugasan_id"],
        status=data.get("status", -1)
    )


# ✅ REMOVE
@router.delete("/profil/{profil_id}/{tugasan_id}")
def remove(profil_id: int, tugasan_id: int, db: Session = Depends(get_db)):
    return remove_tugasan_from_profil(db, profil_id, tugasan_id)



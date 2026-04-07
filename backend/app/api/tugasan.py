from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

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


@router.post("/profil/{profil_id}")
def assign(profil_id: int, payload: dict, db: Session = Depends(get_db)):
    return assign_tugasan_to_profil(
        db,
        profil_id,
        payload["tugasan_id"],
        payload.get("status", -1)
    )
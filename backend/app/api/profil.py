from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.schemas.profil_schema import ProfilCreate, ProfilResponse

from app.services.profil_service import (
    get_profil_by_tapak,
    create_profil
)

router = APIRouter(prefix="/profil", tags=["Profil"])


@router.get("/tapak/{tapak_id}")
def get_by_tapak(tapak_id: int, db: Session = Depends(get_db)):
    return get_profil_by_tapak(db, tapak_id)


@router.post("/", response_model=ProfilResponse)
def create(data: ProfilCreate, db: Session = Depends(get_db)):
    return create_profil(db, data.dict())
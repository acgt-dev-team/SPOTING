from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.schemas.profil_schema import ProfilCreate, ProfilResponse

from app.services.profil_service import (
    get_profil_by_tapak,
    create_profil,
    update_profil,
    delete_profil
)

router = APIRouter(prefix="/profil", tags=["Profil"])


@router.get("/tapak/{tapak_id}", response_model=list[ProfilResponse])
def get_by_tapak(tapak_id: int, db: Session = Depends(get_db)):
    return get_profil_by_tapak(db, tapak_id)


@router.post("/", response_model=ProfilResponse)
def create(data: ProfilCreate, db: Session = Depends(get_db)):
    return create_profil(db, data.dict())


@router.put("/{id}", response_model=ProfilResponse)
def update(id: int, data: ProfilCreate, db: Session = Depends(get_db)):
    updated = update_profil(db, id, data.dict())

    if not updated:
        raise HTTPException(status_code=404, detail="Profil not found")

    return updated


@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    deleted = delete_profil(db, id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Profil not found")

    return {"message": "Deleted"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.schemas.organisasi_schema import (
    OrganisasiCreate,
    OrganisasiResponse
)

from app.services.organisasi_service import (
    create_organisasi,
    get_organisasi_by_pelanggan,
    update_organisasi,
    delete_organisasi
)
from fastapi import HTTPException
from app.models.organisasi import Organisasi
router = APIRouter(prefix="/organisasi", tags=["Organisasi"])


# =========================
# GET
# =========================
@router.get("/pelanggan/{pelanggan_id}", response_model=list[OrganisasiResponse])
def get_by_pelanggan(pelanggan_id: int, db: Session = Depends(get_db)):
    return get_organisasi_by_pelanggan(db, pelanggan_id)


@router.get("/{id}", response_model=OrganisasiResponse)
def get_by_id(id: int, db: Session = Depends(get_db)):
    org = db.query(Organisasi).filter(Organisasi.id == id).first()

    if not org:
        raise HTTPException(status_code=404, detail="Organisasi not found")

    return org

# =========================
# CREATE
# =========================
@router.post("/", response_model=OrganisasiResponse)
def create(data: OrganisasiCreate, db: Session = Depends(get_db)):
    return create_organisasi(db, data.dict())


# =========================
# UPDATE
# =========================
@router.put("/{id}", response_model=OrganisasiResponse)
def update(id: int, data: OrganisasiCreate, db: Session = Depends(get_db)):
    updated = update_organisasi(db, id, data.dict())

    if not updated:
        raise HTTPException(status_code=404, detail="Organisasi not found")

    return updated


# =========================
# DELETE
# =========================
@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    deleted = delete_organisasi(db, id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Organisasi not found")

    return {"message": "Deleted"}
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.schemas.organisasi_schema import (
    OrganisasiCreate,
    OrganisasiResponse
)

from app.services.organisasi_service import (
    create_organisasi,
    get_organisasi_by_pelanggan
)

router = APIRouter(prefix="/organisasi", tags=["Organisasi"])


@router.get("/pelanggan/{pelanggan_id}", response_model=list[OrganisasiResponse])
def get_by_pelanggan(pelanggan_id: int, db: Session = Depends(get_db)):
    return get_organisasi_by_pelanggan(db, pelanggan_id)


@router.post("/", response_model=OrganisasiResponse)
def create(data: OrganisasiCreate, db: Session = Depends(get_db)):
    return create_organisasi(db, data.dict())
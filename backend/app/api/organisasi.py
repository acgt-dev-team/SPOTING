from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.services.organisasi_service import (
    get_organisasi_by_pelanggan,
    create_organisasi
)

router = APIRouter(prefix="/organisasi", tags=["Organisasi"])


@router.get("/pelanggan/{pelanggan_id}")
def get_by_pelanggan(pelanggan_id: int, db: Session = Depends(get_db)):
    try:
        return get_organisasi_by_pelanggan(db, pelanggan_id)
    except Exception as e:
        print("🔥 API ERROR:", str(e))
        raise e


@router.post("/")
def create(data: dict, db: Session = Depends(get_db)):
    try:
        return create_organisasi(db, data)
    except Exception as e:
        print("🔥 CREATE ERROR:", str(e))
        raise e
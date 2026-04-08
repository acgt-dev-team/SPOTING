from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.services.sub_organisasi_service import (
    get_sub_by_organisasi,
    create_sub_organisasi
)

router = APIRouter(prefix="/sub-organisasi", tags=["Sub Organisasi"])


@router.get("/organisasi/{organisasi_id}")
def get_by_organisasi(organisasi_id: int, db: Session = Depends(get_db)):
    try:
        return get_sub_by_organisasi(db, organisasi_id)
    except Exception as e:
        print("🔥 API ERROR:", str(e))
        raise e


@router.post("/")
def create(data: dict, db: Session = Depends(get_db)):
    try:
        return create_sub_organisasi(db, data)
    except Exception as e:
        print("🔥 CREATE ERROR:", str(e))
        raise e
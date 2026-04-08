from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.services.tapak_service import (
    get_tapak_by_sub,
    create_tapak
)

router = APIRouter(prefix="/tapak", tags=["Tapak"])


@router.get("/sub/{sub_id}")
def get_by_sub(sub_id: int, db: Session = Depends(get_db)):
    try:
        return get_tapak_by_sub(db, sub_id)
    except Exception as e:
        print("🔥 API ERROR:", str(e))
        raise e


@router.post("/")
def create(data: dict, db: Session = Depends(get_db)):
    try:
        return create_tapak(db, data)
    except Exception as e:
        print("🔥 API CREATE ERROR:", str(e))
        raise e
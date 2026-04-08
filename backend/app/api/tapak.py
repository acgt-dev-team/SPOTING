from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.schemas.tapak_schema import TapakCreate, TapakResponse

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


@router.post("/", response_model=TapakResponse)
def create(data: TapakCreate, db: Session = Depends(get_db)):
    return create_tapak(db, data.dict())
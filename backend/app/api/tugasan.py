from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.schemas.tugasan_schema import TugasanCreate, TugasanResponse

from app.services.tugasan_service import (
    get_tugasan_by_profil,
    assign_tugasan_to_profil,
    remove_tugasan_from_profil,
    get_all_tugasan,
    create_tugasan,
    update_tugasan,
    execute_scan
)
from app.i18n import t

router = APIRouter(prefix="/tugasan", tags=[t("docs.tags.task")])


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
        tugasan_id=data["tugasan_id"]
    )


# ✅ REMOVE
@router.delete("/profil/{profil_id}/{tugasan_id}")
def remove_tugasan(profil_id: int, tugasan_id: int, db: Session = Depends(get_db)):
    return remove_tugasan_from_profil(db, profil_id, tugasan_id)


@router.post("/", response_model=TugasanResponse)
def create(data: TugasanCreate, db: Session = Depends(get_db)):
    return create_tugasan(db, data.dict())

@router.put("/{tugasan_id}")
def update(
    tugasan_id: int,
    data: TugasanCreate,
    db: Session = Depends(get_db)
):
    return update_tugasan(
        db,
        tugasan_id=tugasan_id,
        data=data.dict()
    )

@router.post("/execute-scan")
def run_scan(data: dict, db: Session = Depends(get_db)):
    return execute_scan(
        db=db,
        profil_tugasan_id=data["profil_tugasan_id"],
        penjadualan=data.get("penjadualan", False)
    )

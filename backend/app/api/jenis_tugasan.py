from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.services.jenis_tugasan_service import get_all_jenis
from app.i18n import t

router = APIRouter(prefix="/jenis_tugasan", tags=[t("docs.tags.taskType")])


@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return get_all_jenis(db)

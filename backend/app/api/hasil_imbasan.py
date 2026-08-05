from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.hasil_imbasan import (
    HasilImbasanCreate,
    HasilImbasanResponse
)

from app.services.hasil_imbasan_service import (
    create_hasil_imbasan
)
from app.i18n import t

router = APIRouter(
    prefix="/ejen",
    tags=[t("docs.tags.scanResult")]
)


@router.post(
    "/hasil",
    response_model=HasilImbasanResponse
)
def save_scan_result(
    request: HasilImbasanCreate,
    db: Session = Depends(get_db)
):
    return create_hasil_imbasan(
        db,
        request
    )

@router.post("/hasil/gagal/{profil_tugasan_ejen_id}")
def mark_failed(
    profil_tugasan_ejen_id: int,
    db: Session = Depends(get_db)
):
    from app.services.hasil_imbasan_service import mark_task_failed

    return mark_task_failed(
        db,
        profil_tugasan_ejen_id
    )

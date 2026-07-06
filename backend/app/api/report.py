from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from app.database.session import get_db
from app.services.report_service import generate_report
from app.i18n import t

router = APIRouter(
    prefix="/report",
    tags=[t("docs.tags.report")]
)


@router.post("/profil/{profil_id}")
def generate(
    profil_id: int,
    db: Session = Depends(get_db)
):

    result = generate_report(db, profil_id)

    if "file" not in result:
        return result

    return FileResponse(
        path=result["file"],
        filename=result["file"].split("/")[-1],
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

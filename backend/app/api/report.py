from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from app.database.session import get_db
from app.services.report_service import generate_report
from app.i18n import t

router = APIRouter(
    prefix="/report",
    tags=[t("docs.tags.report")]
)


class ReportFormat(str, Enum):
    default = "default"
    cyclonedx = "cyclonedx"


@router.post("/profil/{profil_id}")
def generate(
    profil_id: int,
    report_format: ReportFormat = Query(
        default=ReportFormat.default,
        alias="format",
    ),
    db: Session = Depends(get_db)
):

    result = generate_report(db, profil_id, report_format.value)

    if "file" not in result:
        raise HTTPException(status_code=404, detail=result["message"])

    return FileResponse(
        path=result["file"],
        filename=result["file"].split("/")[-1],
        media_type=result["media_type"]
    )

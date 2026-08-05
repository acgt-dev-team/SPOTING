from enum import Enum
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.i18n import t
from app.services.report_service import generate_report


router = APIRouter(
    prefix="/report",
    tags=[t("docs.tags.report")],
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
    db: Session = Depends(get_db),
):
    """
    Generate and download a report for a profile.
    """

    try:
        result = generate_report(
            db=db,
            profil_id=profil_id,
            report_format=report_format.value,
        )

    except Exception as exc:
        # Optional: log the exception here
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate report: {str(exc)}",
        )

    #
    # Report service returned an error
    #
    if "file" not in result:
        raise HTTPException(
            status_code=404,
            detail=result.get(
                "message",
                t("report.noResults"),
            ),
        )

    report_path = Path(result["file"])

    #
    # Safety check
    #
    if not report_path.exists():
        raise HTTPException(
            status_code=500,
            detail="Generated report file not found.",
        )

    return FileResponse(
        path=str(report_path),
        filename=report_path.name,
        media_type=result["media_type"],
    )

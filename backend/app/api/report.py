from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.report_service import generate_report
from fastapi.responses import FileResponse

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)

@router.post("/profil/{profil_id}")
def generate(profil_id: int, db: Session = Depends(get_db)):

    result = generate_report(db, profil_id)

    if "file" not in result:
        return result

    return FileResponse(
        path=result["file"],
        filename=result["file"],
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
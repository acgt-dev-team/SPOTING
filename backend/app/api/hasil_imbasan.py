from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.session import get_db

router = APIRouter(
    prefix="/hasil-imbasan",
    tags=["Hasil Imbasan"]
)


@router.get("/{profil_tugasan_id}")
def get_scan_results(profil_tugasan_id: int, db: Session = Depends(get_db)):
    results = db.execute(
        text("""
            SELECT id, created_at, data_imbasan
            FROM hasil_imbasan
            WHERE x_profil_tugasan_id = :id
            ORDER BY created_at DESC
        """),
        {"id": profil_tugasan_id}
    ).fetchall()

    return [
        {
            "id": row.id,
            "created_at": row.created_at,
            "data_imbasan": row.data_imbasan
        }
        for row in results
    ]
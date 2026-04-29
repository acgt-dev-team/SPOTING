from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.session import get_db
from app.models.organisasi import Organisasi
from app.models.sub_organisasi import SubOrganisasi
from app.models.tapak import Tapak
from app.models.profil import Profil
from app.models.tugasan import Tugasan

router = APIRouter(
    prefix="/api",
    tags=["Dashboard"]
)


@router.get("/dashboard")
def get_dashboard_stats(
    db: Session = Depends(get_db)
):
    total_organisasi = db.query(
        func.count(Organisasi.id)
    ).scalar()

    total_sub_organisasi = db.query(
        func.count(SubOrganisasi.id)
    ).scalar()

    total_tapak = db.query(
        func.count(Tapak.id)
    ).scalar()

    total_profil = db.query(
        func.count(Profil.id)
    ).scalar()

    total_tugasan = db.query(
        func.count(Tugasan.id)
    ).scalar()

    return {
        "organisasi": total_organisasi,
        "sub_organisasi": total_sub_organisasi,
        "tapak": total_tapak,
        "profil": total_profil,
        "tugasan": total_tugasan
    }
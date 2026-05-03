from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.organisasi import Organisasi
from app.models.sub_organisasi import SubOrganisasi
from app.models.tapak import Tapak
from app.models.profil import Profil
from app.models.tugasan import Tugasan
from app.models.x_profil_tugasan import XProfilTugasan



def get_dashboard_stats(db: Session):

    organisasi_count = db.query(func.count(Organisasi.id)).scalar()
    sub_organisasi_count = db.query(func.count(SubOrganisasi.id)).scalar()
    tapak_count = db.query(func.count(Tapak.id)).scalar()
    profil_count = db.query(func.count(Profil.id)).scalar()
    tugasan_count = db.query(func.count(Tugasan.id)).scalar()

    return {
        "organisasi": organisasi_count or 0,
        "sub_organisasi": sub_organisasi_count or 0,
        "tapak": tapak_count or 0,
        "profil": profil_count or 0,
        "tugasan": tugasan_count or 0
    }

def get_organization_performance(db: Session):
    results = (
        db.query(
            Organisasi,
            func.count(XProfilTugasan.id).label("total"),
            func.count(XProfilTugasan.id).filter(
                XProfilTugasan.status_id == 3
            ).label("done")
        )
        .outerjoin(SubOrganisasi, SubOrganisasi.organisasi_id == Organisasi.id)
        .outerjoin(Tapak, Tapak.sub_organisasi_id == SubOrganisasi.id)
        .outerjoin(Profil, Profil.tapak_id == Tapak.id)
        .outerjoin(XProfilTugasan, XProfilTugasan.profil_id == Profil.id)
        .group_by(Organisasi.id)
        .all()
    )

    response = []

    for i, (org, total, done) in enumerate(results, start=1):
        response.append({
            "bil": i,
            "nama": org.nama,
            "total": total or 0,
            "done": done or 0
        })

    return response
from sqlalchemy.orm import Session
from app.models.profil import Profil


def get_profil_by_tapak(db: Session, tapak_id: int):
    profils = db.query(Profil).filter(Profil.tapak_id == tapak_id).all()

    result = []
    for p in profils:
        result.append({
            "id": p.id,
            "nama": p.nama,
            "deskripsi": p.deskripsi,
            "kod": p.kod,
            "aktif": p.aktif
        })

    return result
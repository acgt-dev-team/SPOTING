from sqlalchemy.orm import Session
from app.models.profil import Profil


def get_profil_by_tapak(db: Session, tapak_id: int):
    profils = db.query(Profil).filter(Profil.tapak_id == tapak_id).all()

    result = []
    for p in profils:
        result.append({
            "id": p.id,
            "nama": p.nama,
            "deskripsi": p.keterangan,  # ✅ map DB → frontend
            "kod": p.kod,
            "aktif": p.aktif
        })

    return result


def create_profil(db: Session, data: dict):
    new_profil = Profil(
        tapak_id=data["tapak_id"],
        kod=data["kod"],
        nama=data["nama"],
        keterangan=data.get("deskripsi", "")  # ✅ map frontend → DB
    )

    db.add(new_profil)
    db.commit()
    db.refresh(new_profil)

    return {
        "id": new_profil.id,
        "nama": new_profil.nama,
        "deskripsi": new_profil.keterangan
    }
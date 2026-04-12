from sqlalchemy.orm import Session
from app.models.profil import Profil


def get_profil_by_tapak(db: Session, tapak_id: int):
    profils = db.query(Profil).filter(Profil.tapak_id == tapak_id).all()

    result = []
    for p in profils:
        result.append({
            "id": p.id,
            "tapak_id": p.tapak_id,   # ✅ ADD THIS
            "nama": p.nama,
            "keterangan": p.keterangan,
            "kod": p.kod,
            "aktif": bool(p.aktif) if p.aktif is not None else False
        })

    return result


def create_profil(db: Session, data: dict):
    new_profil = Profil(
        tapak_id=data["tapak_id"],
        kod=data["kod"],
        nama=data["nama"],
        keterangan=data.get("keterangan", "")  # ✅ map frontend → DB
    )

    db.add(new_profil)
    db.commit()
    db.refresh(new_profil)

    return {
    "id": new_profil.id,
    "tapak_id": new_profil.tapak_id,
    "kod": new_profil.kod,
    "nama": new_profil.nama,
    "keterangan": new_profil.keterangan,
    "aktif": bool(new_profil.aktif) if new_profil.aktif is not None else False
}

# =========================
# UPDATE
# =========================
def update_profil(db: Session, id: int, data: dict):
    profil = db.query(Profil).filter(Profil.id == id).first()

    if not profil:
        return None

    profil.nama = data["nama"]
    profil.kod = data["kod"]
    profil.keterangan = data.get("keterangan", "")

    db.commit()
    db.refresh(profil)

    return {
        "id": profil.id,
        "tapak_id": profil.tapak_id,
        "kod": profil.kod,
        "nama": profil.nama,
        "keterangan": profil.keterangan,
        "aktif": bool(profil.aktif) if profil.aktif is not None else False
    }


# =========================
# DELETE
# =========================
def delete_profil(db: Session, id: int):
    profil = db.query(Profil).filter(Profil.id == id).first()

    if not profil:
        return False

    db.delete(profil)
    db.commit()
    return True
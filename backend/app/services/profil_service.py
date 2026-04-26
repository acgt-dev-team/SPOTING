from sqlalchemy.orm import Session
from app.models.profil import Profil
import re
from sqlalchemy import func
from app.models.x_profil_tugasan import XProfilTugasan

def get_profil_by_tapak(db: Session, tapak_id: int):
    profils = (
        db.query(
            Profil,
            func.count(
                func.distinct(XProfilTugasan.tugasan_id)
            ).label("tugasan_count")
        )
        .outerjoin(
            XProfilTugasan,
            XProfilTugasan.profil_id == Profil.id
        )
        .filter(
            Profil.tapak_id == tapak_id
        )
        .group_by(Profil.id)
        .all()
    )

    return [
        {
            "id": profil.id,
            "tapak_id": profil.tapak_id,
            "nama": profil.nama,
            "keterangan": profil.keterangan,
            "kod": profil.kod,
            "aktif": bool(profil.aktif) if profil.aktif is not None else False,
            "tugasan_count": tugasan_count
        }
        for profil, tugasan_count in profils
    ]


#create

def generate_next_profil_kod(db: Session):
    latest_profile = (
        db.query(Profil)
        .filter(Profil.kod.like("PRF%"))
        .order_by(Profil.id.desc())
        .first()
    )

    if not latest_profile:
        return "PRF001"

    match = re.search(r"PRF(\d+)", latest_profile.kod)

    if not match:
        return "PRF001"

    next_number = int(match.group(1)) + 1

    return f"PRF{next_number:03d}"

def create_profil(db: Session, data: dict):
    new_profil = Profil(
        tapak_id=data["tapak_id"],
        kod=generate_next_profil_kod(db),
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
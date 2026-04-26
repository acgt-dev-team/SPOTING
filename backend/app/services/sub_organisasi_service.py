from sqlalchemy.orm import Session
from app.models.sub_organisasi import SubOrganisasi
import re
from sqlalchemy import func
from app.models.tapak import Tapak

# =========================
# GET
# =========================
def get_sub_by_organisasi(db: Session, organisasi_id: int):
    subs = (
        db.query(
            SubOrganisasi,
            func.count(func.distinct(Tapak.id)).label("tapak_count")
        )
        .outerjoin(
            Tapak,
            Tapak.sub_organisasi_id == SubOrganisasi.id
        )
        .filter(
            SubOrganisasi.organisasi_id == organisasi_id
        )
        .group_by(SubOrganisasi.id)
        .all()
    )

    return [
        {
            "id": sub.id,
            "organisasi_id": sub.organisasi_id,
            "nama": sub.nama,
            "keterangan": sub.keterangan,
            "kod": sub.kod,
            "pegawai_tadbir": sub.pegawai_tadbir,
            "jawatan": sub.jawatan,
            "aktif": bool(sub.aktif) if sub.aktif is not None else False,
            "tapak_count": tapak_count
        }
        for sub, tapak_count in subs
    ]


# =========================
# CREATE
# =========================
def generate_next_sub_kod(db: Session):
    latest_sub = (
        db.query(SubOrganisasi)
        .filter(SubOrganisasi.kod.like("SUB%"))
        .order_by(SubOrganisasi.id.desc())
        .first()
    )

    if not latest_sub:
        return "SUB001"

    match = re.search(r"SUB(\d+)", latest_sub.kod)

    if not match:
        return "SUB001"

    next_number = int(match.group(1)) + 1

    return f"SUB{next_number:03d}"

def create_sub_organisasi(db: Session, data: dict):
    new_sub = SubOrganisasi(
        organisasi_id=data["organisasi_id"],
        kod=generate_next_sub_kod(db),
        nama=data["nama"],
        keterangan=data.get("keterangan", ""),
        pegawai_tadbir=data.get("pegawai_tadbir"),  # ✅ OK
        jawatan=data.get("jawatan")                 # ✅ OK
    )

    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)

    return {
        "id": new_sub.id,
        "organisasi_id": new_sub.organisasi_id,
        "kod": new_sub.kod,
        "nama": new_sub.nama,
        "keterangan": new_sub.keterangan,
        "pegawai_tadbir": new_sub.pegawai_tadbir,   # ✅ FIXED
        "jawatan": new_sub.jawatan,                 # ✅ FIXED
        "aktif": bool(new_sub.aktif) if new_sub.aktif is not None else False
    }


# =========================
# UPDATE
# =========================
def update_sub_organisasi(db: Session, id: int, data: dict):
    sub = db.query(SubOrganisasi).filter(SubOrganisasi.id == id).first()

    if not sub:
        return None

    sub.nama = data["nama"]
    sub.keterangan = data.get("keterangan", "")
    sub.pegawai_tadbir = data.get("pegawai_tadbir")   # ✅ FIXED
    sub.jawatan = data.get("jawatan")                 # ✅ FIXED

    db.commit()
    db.refresh(sub)

    return {
        "id": sub.id,
        "organisasi_id": sub.organisasi_id,
        "kod": sub.kod,
        "nama": sub.nama,
        "keterangan": sub.keterangan,
        "pegawai_tadbir": sub.pegawai_tadbir,
        "jawatan": sub.jawatan,
        "aktif": bool(sub.aktif) if sub.aktif is not None else False
    }


# =========================
# DELETE
# =========================
def delete_sub_organisasi(db: Session, id: int):
    sub = db.query(SubOrganisasi).filter(SubOrganisasi.id == id).first()

    if not sub:
        return False

    db.delete(sub)
    db.commit()
    return True
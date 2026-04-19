from sqlalchemy.orm import Session
from app.models.sub_organisasi import SubOrganisasi


# =========================
# GET
# =========================
def get_sub_by_organisasi(db: Session, organisasi_id: int):
    subs = db.query(SubOrganisasi).filter(
        SubOrganisasi.organisasi_id == organisasi_id
    ).all()

    return [
        {
            "id": s.id,
            "organisasi_id": s.organisasi_id,
            "nama": s.nama,
            "keterangan": s.keterangan,
            "kod": s.kod,
            "pegawai_tadbir": s.pegawai_tadbir,   # ✅ FIXED
            "jawatan": s.jawatan,                 # ✅ FIXED
            "aktif": bool(s.aktif) if s.aktif is not None else False
        }
        for s in subs
    ]


# =========================
# CREATE
# =========================
def create_sub_organisasi(db: Session, data: dict):
    new_sub = SubOrganisasi(
        organisasi_id=data["organisasi_id"],
        kod=data["kod"],
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
    sub.kod = data["kod"]
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
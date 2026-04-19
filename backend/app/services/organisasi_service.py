from sqlalchemy.orm import Session
from app.models.organisasi import Organisasi


# =========================
# GET
# =========================
def get_organisasi_by_pelanggan(db: Session, pelanggan_id: int):
    organisasis = db.query(Organisasi).filter(
        Organisasi.pelanggan_id == pelanggan_id
    ).all()

    return [
        {
            "id": o.id,
            "pelanggan_id": o.pelanggan_id,
            "nama": o.nama,
            "keterangan": o.keterangan,
            "kod": o.kod,
            "pegawai_tadbir": o.pegawai_tadbir,
            "jawatan": o.jawatan,
            "aktif": bool(o.aktif) if o.aktif is not None else False
        }
        for o in organisasis
    ]


# =========================
# CREATE
# =========================
def create_organisasi(db: Session, data: dict):
    new_org = Organisasi(
    pelanggan_id=data["pelanggan_id"],
    kod=data["kod"],
    nama=data["nama"],
    keterangan=data.get("keterangan", ""),
    pegawai_tadbir=data.get("pegawai_tadbir"),
    jawatan=data.get("jawatan")
)

    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    return {
        "id": new_org.id,
        "pelanggan_id": new_org.pelanggan_id,
        "kod": new_org.kod,
        "nama": new_org.nama,
        "keterangan": new_org.keterangan,
        "aktif": bool(new_org.aktif) if new_org.aktif is not None else False
    }


# =========================
# UPDATE
# =========================
def update_organisasi(db: Session, id: int, data: dict):
    org = db.query(Organisasi).filter(Organisasi.id == id).first()

    if not org:
        return None

    org.nama = data["nama"]
    org.kod = data["kod"]
    org.keterangan = data.get("keterangan", "")
    org.pegawai_tadbir = data.get("pegawai_tadbir")
    org.jawatan = data.get("jawatan")

    db.commit()
    db.refresh(org)

    return {
    "id": org.id,
    "pelanggan_id": org.pelanggan_id,
    "kod": org.kod,
    "nama": org.nama,
    "keterangan": org.keterangan,
    "pegawai_tadbir": org.pegawai_tadbir,
    "jawatan": org.jawatan,
    "aktif": bool(org.aktif) if org.aktif is not None else False
    }


# =========================
# DELETE
# =========================
def delete_organisasi(db: Session, id: int):
    org = db.query(Organisasi).filter(Organisasi.id == id).first()

    if not org:
        return False

    db.delete(org)
    db.commit()
    return True
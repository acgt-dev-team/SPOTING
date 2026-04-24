from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.organisasi import Organisasi
from app.models.sub_organisasi import SubOrganisasi
from app.models.tapak import Tapak


# =========================
# GET
# =========================
def get_organisasi_by_pelanggan(db: Session, pelanggan_id: int):
    organisasis = (
        db.query(
            Organisasi,
            func.count(func.distinct(SubOrganisasi.id)).label("sub_count"),
            func.count(func.distinct(Tapak.id)).label("tapak_count")
        )
        .outerjoin(
            SubOrganisasi,
            SubOrganisasi.organisasi_id == Organisasi.id
        )
        .outerjoin(
            Tapak,
            Tapak.sub_organisasi_id == SubOrganisasi.id
        )
        .filter(
            Organisasi.pelanggan_id == pelanggan_id
        )
        .group_by(Organisasi.id)
        .all()
    )
    print(organisasis)

    return [
        {
            "id": org.id,
            "pelanggan_id": org.pelanggan_id,
            "nama": org.nama,
            "keterangan": org.keterangan,
            "kod": org.kod,
            "pegawai_tadbir": org.pegawai_tadbir,
            "jawatan": org.jawatan,
            "aktif": bool(org.aktif) if org.aktif is not None else False,
            "sub_count": sub_count,
            "tapak_count": tapak_count
        }
        for org, sub_count, tapak_count in organisasis
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
from sqlalchemy.orm import Session
from sqlalchemy import func
import re

from app.models.organisasi import Organisasi
from app.models.sub_organisasi import SubOrganisasi
from app.models.tapak import Tapak
from app.models.profil import Profil
from app.models.x_profil_tugasan import XProfilTugasan

# =========================
# GET
# =========================
def get_organisasi_by_pelanggan(db: Session, pelanggan_id: int):
    organisasis = (
        db.query(
            Organisasi,
            func.count(func.distinct(SubOrganisasi.id)).label("sub_count"),
            func.count(func.distinct(Tapak.id)).label("tapak_count"),
            func.count(func.distinct(XProfilTugasan.tugasan_id)).label("tugasan_count")
        )
        .outerjoin(
            SubOrganisasi,
            SubOrganisasi.organisasi_id == Organisasi.id
        )
        .outerjoin(
            Tapak,
            Tapak.sub_organisasi_id == SubOrganisasi.id
        )
        .outerjoin(
            Profil,
            Profil.tapak_id == Tapak.id
        )
        .outerjoin(
            XProfilTugasan,
            XProfilTugasan.profil_id == Profil.id
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
            "tapak_count": tapak_count,
            "tugasan_count": tugasan_count,
        }
        for org, sub_count, tapak_count, tugasan_count in organisasis
    ]


# =========================
# CREATE
# =========================
def generate_next_org_kod(db: Session):
    latest_org = (
        db.query(Organisasi)
        .filter(Organisasi.kod.like("ORG%"))
        .order_by(Organisasi.id.desc())
        .first()
    )

    if not latest_org:
        return "ORG001"

    match = re.search(r"ORG(\d+)", latest_org.kod)

    if not match:
        return "ORG001"

    next_number = int(match.group(1)) + 1

    return f"ORG{next_number:03d}"

def create_organisasi(db: Session, data: dict):
    new_org = Organisasi(
        pelanggan_id=data["pelanggan_id"],
        kod=generate_next_org_kod(db),
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
    org.keterangan = data.get("keterangan", "")
    org.pegawai_tadbir = data.get("pegawai_tadbir")
    org.jawatan = data.get("jawatan")

    db.commit()
    db.refresh(org)

    return {
        "id": org.id,
        "pelanggan_id": org.pelanggan_id,
        "kod": org.kod,   # ← add this
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
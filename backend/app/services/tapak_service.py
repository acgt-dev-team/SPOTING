from sqlalchemy.orm import Session
from app.models.tapak import Tapak
import re
from sqlalchemy import func
from app.models.profil import Profil
from app.models.x_profil_tugasan import XProfilTugasan

# =========================
# GET
# =========================
def get_tapak_by_sub(db: Session, sub_id: int):
    sites = (
        db.query(
            Tapak,
            func.count(
                func.distinct(XProfilTugasan.tugasan_id)
            ).label("tugasan_count")
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
            Tapak.sub_organisasi_id == sub_id
        )
        .group_by(Tapak.id)
        .all()
    )

    return [
        {
            "id": site.id,
            "sub_organisasi_id": site.sub_organisasi_id,
            "kod": site.kod,
            "nama": site.nama,
            "keterangan": site.keterangan,
            "pegawai_tadbir": site.pegawai_tadbir,
            "jawatan": site.jawatan,
            "aktif": bool(site.aktif) if site.aktif is not None else False,
            "tugasan_count": tugasan_count
        }
        for site, tugasan_count in sites
    ]


# =========================
# CREATE
# =========================
def generate_next_tapak_kod(db: Session):
    latest_site = (
        db.query(Tapak)
        .filter(Tapak.kod.like("TPK%"))
        .order_by(Tapak.id.desc())
        .first()
    )

    if not latest_site:
        return "TPK001"

    match = re.search(r"TPK(\d+)", latest_site.kod)

    if not match:
        return "TPK001"

    next_number = int(match.group(1)) + 1

    return f"TPK{next_number:03d}"

def create_tapak(db: Session, data: dict):
    new_site = Tapak(
        sub_organisasi_id=data["sub_organisasi_id"],
        kod=generate_next_tapak_kod(db),
        nama=data["nama"],
        pegawai_tadbir=data.get("pegawai_tadbir"),
        jawatan=data.get("jawatan"),
        keterangan=data.get("keterangan", "")
        
    )

    db.add(new_site)
    db.commit()
    db.refresh(new_site)

    return {
        "id": new_site.id,
        "sub_organisasi_id": new_site.sub_organisasi_id,
        "kod": new_site.kod,
        "nama": new_site.nama,
        "keterangan": new_site.keterangan,
        "pegawai_tadbir": new_site.pegawai_tadbir,
        "jawatan": new_site.jawatan,
        "aktif": bool(new_site.aktif) if new_site.aktif is not None else False
    }


# =========================
# UPDATE
# =========================
def update_tapak(db: Session, id: int, data: dict):
    site = db.query(Tapak).filter(Tapak.id == id).first()

    if not site:
        return None

    site.nama = data["nama"]
    site.keterangan = data.get("keterangan", "")
    site.pegawai_tadbir = data.get("pegawai_tadbir")
    site.jawatan = data.get("jawatan")

    db.commit()
    db.refresh(site)

    return {
        "id": site.id,
        "sub_organisasi_id": site.sub_organisasi_id,
        "kod": site.kod,
        "nama": site.nama,
        "keterangan": site.keterangan,
        "pegawai_tadbir": site.pegawai_tadbir,
        "jawatan": site.jawatan,
        "aktif": bool(site.aktif) if site.aktif is not None else False
    }


# =========================
# DELETE
# =========================
def delete_tapak(db: Session, id: int):
    site = db.query(Tapak).filter(Tapak.id == id).first()

    if not site:
        return False

    db.delete(site)
    db.commit()
    return True
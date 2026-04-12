from sqlalchemy.orm import Session
from app.models.tapak import Tapak


# =========================
# GET
# =========================
def get_tapak_by_sub(db: Session, sub_id: int):
    sites = db.query(Tapak).filter(
        Tapak.sub_organisasi_id == sub_id
    ).all()

    return [
        {
            "id": s.id,
            "sub_organisasi_id": s.sub_organisasi_id,
            "kod": s.kod,
            "nama": s.nama,
            "keterangan": s.keterangan,
            "aktif": bool(s.aktif) if s.aktif is not None else False
        }
        for s in sites
    ]


# =========================
# CREATE
# =========================
def create_tapak(db: Session, data: dict):
    new_site = Tapak(
        sub_organisasi_id=data["sub_organisasi_id"],
        kod=data["kod"],
        nama=data["nama"],
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
    site.kod = data["kod"]
    site.keterangan = data.get("keterangan", "")

    db.commit()
    db.refresh(site)

    return {
        "id": site.id,
        "sub_organisasi_id": site.sub_organisasi_id,
        "kod": site.kod,
        "nama": site.nama,
        "keterangan": site.keterangan,
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
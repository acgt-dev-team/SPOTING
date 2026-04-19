from sqlalchemy.orm import Session
from app.models.tugasan import Tugasan
from app.models.x_profil_tugasan import XProfilTugasan


# =========================
# GET ASSIGNED
# =========================
def get_tugasan_by_profil(db: Session, profil_id: int):
    results = (
        db.query(XProfilTugasan)
        .filter(XProfilTugasan.profil_id == profil_id)
        .all()
    )

    response = []
    for item in results:
        response.append({
    "id": item.tugasan.id,
    "nama": item.tugasan.nama,
    "kod": item.tugasan.kod,
    "keterangan": item.tugasan.keterangan,
    "protocol": item.tugasan.protocol,
    "ip_start": item.tugasan.ip_start,
    "ip_end": item.tugasan.ip_end,
    "status": item.status
})

    return response


# =========================
# ASSIGN
# =========================
def assign_tugasan_to_profil(db: Session, profil_id: int, tugasan_id: int, status: int = -1):
    existing = db.query(XProfilTugasan).filter_by(
        profil_id=profil_id,
        tugasan_id=tugasan_id
    ).first()

    if existing:
        return {"message": "Already assigned"}

    new_item = XProfilTugasan(
        profil_id=profil_id,
        tugasan_id=tugasan_id,
        status=status
    )

    db.add(new_item)
    db.commit()

    return {"message": "Assigned successfully"}

def create_tugasan(db: Session, data: dict):
    new_tugasan = Tugasan(
        nama=data["nama"],
        kod=data["kod"],
        keterangan=data.get("keterangan"),
        jenis_id=data["jenis_id"],
        protocol=data.get("protocol"),
        ip_start=data.get("ip_start"),
        ip_end=data.get("ip_end"),
        aktif=data.get("aktif", True)
    )

    db.add(new_tugasan)
    db.commit()
    db.refresh(new_tugasan)

    return {
    "id": new_tugasan.id,
    "nama": new_tugasan.nama,
    "kod": new_tugasan.kod,
    "keterangan": new_tugasan.keterangan,
    "jenis_id": new_tugasan.jenis_id,
    "protocol": new_tugasan.protocol,
    "ip_start": new_tugasan.ip_start,
    "ip_end": new_tugasan.ip_end,
    "aktif": new_tugasan.aktif
    }

# =========================
# REMOVE
# =========================
def remove_tugasan_from_profil(db: Session, profil_id: int, tugasan_id: int):
    item = db.query(XProfilTugasan).filter_by(
        profil_id=profil_id,
        tugasan_id=tugasan_id
    ).first()

    if item:
        db.delete(item)
        db.commit()

    return {"message": "Removed"}


# =========================
# GET ALL (FOR DROPDOWN)
# =========================
def get_all_tugasan(db: Session):
    tugasan = db.query(Tugasan).all()

    return [
        {
            "id": t.id,
            "nama": t.nama,
            "kod": t.kod,
            "keterangan": t.keterangan,
            "protocol": t.protocol,
            "ip_start": t.ip_start, 
            "ip_end": t.ip_end,
            "aktif": bool(t.aktif) if t.aktif is not None else False,
            "jenis_id": t.jenis_id
        }
        for t in tugasan
    ]

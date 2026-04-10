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
            "nama": getattr(item.tugasan, "nama", ""),
            "keterangan": getattr(item.tugasan, "keterangan", ""),  # ✅ SAFE
            "status": item.status,
            "jadualkan_pada": item.jadualkan_pada,
            "selesai_pada": item.selesai_pada
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


# =========================
# REMOVE
# =========================
def remove_tugasan_from_profil(db: Session, profil_id: int, tugasan_id: int):
    item = db.query(XProfilTugasan).filter_by(
        profil_id=profil_id,
        tugasan_id=tugasan_id
    ).first()

    if not item:
        return {"message": "Not found"}

    db.delete(item)
    db.commit()

    return {"message": "Removed successfully"}


# =========================
# GET ALL (FOR DROPDOWN)
# =========================
def get_all_tugasan(db: Session):
    tugasan_list = db.query(Tugasan).all()

    return [
        {
            "id": t.id,
            "nama": getattr(t, "nama", ""),
            "kod": getattr(t, "kod", ""),
            "keterangan": getattr(t, "keterangan", "")
        }
        for t in tugasan_list
    ]


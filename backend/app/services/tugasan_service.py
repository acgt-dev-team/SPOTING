from sqlalchemy.orm import Session
from app.models.tugasan import Tugasan
from app.models.x_profil_tugasan import XProfilTugasan


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
            "keterangan": item.tugasan.protocol,  # adjust if needed
            "status": item.status,
            "jadualkan_pada": item.jadualkan_pada,
            "selesai_pada": item.selesai_pada
        })

    return response


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


def get_all_tugasan(db: Session):
    return db.query(Tugasan).all()
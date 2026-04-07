from sqlalchemy.orm import Session
from app.models.profil import Profil


def get_profil_by_tapak(db: Session, tapak_id: int):
    return db.query(Profil).filter(Profil.tapak_id == tapak_id).all()


def create_profil(db: Session, data: dict):
    new_profil = Profil(
        tapak_id=data["tapak_id"],
        kod=data["kod"],
        nama=data["nama"],
        deskripsi=data.get("deskripsi", "")
    )

    db.add(new_profil)
    db.commit()
    db.refresh(new_profil)

    return new_profil
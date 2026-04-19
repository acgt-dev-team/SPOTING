from sqlalchemy.orm import Session
from app.models.jenis_tugasan import JenisTugasan

def get_all_jenis(db: Session):
    jenis = db.query(JenisTugasan).all()

    return [
        {
            "id": j.id,
            "nama": j.nama
        }
        for j in jenis
    ]
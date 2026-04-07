from sqlalchemy.orm import Session
from app.models.tapak import Tapak


def get_tapak_by_sub(db: Session, sub_id: int):
    tapaks = db.query(Tapak).filter(Tapak.sub_organisasi_id == sub_id).all()

    result = []
    for t in tapaks:
        result.append({
            "id": t.id,
            "nama": t.nama,
            "keterangan": t.deskripsi,
            "kod": t.kod,
            "aktif": t.aktif
        })

    return result


def create_tapak(db: Session, data: dict):
    new_tapak = Tapak(
        sub_organisasi_id=data["sub_organisasi_id"],
        kod=data["kod"],
        nama=data["nama"],
        deskripsi=data.get("keterangan", "")
    )

    db.add(new_tapak)
    db.commit()
    db.refresh(new_tapak)

    return {
        "id": new_tapak.id,
        "nama": new_tapak.nama,
        "keterangan": new_tapak.deskripsi
    }
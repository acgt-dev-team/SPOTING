from sqlalchemy.orm import Session
from app.models.organisasi import Organisasi


def get_organisasi_by_pelanggan(db: Session, pelanggan_id: int):
    organisasis = db.query(Organisasi).filter(
        Organisasi.pelanggan_id == pelanggan_id
    ).all()

    return [
        {
            "id": o.id,
            "nama": o.nama,
            "keterangan": o.keterangan,
            "kod": o.kod,
            "aktif": o.aktif
        }
        for o in organisasis
    ]


def create_organisasi(db: Session, data: dict):
    new_org = Organisasi(
        pelanggan_id=data["pelanggan_id"],
        kod=data["kod"],
        nama=data["nama"],
        keterangan=data.get("keterangan", "")
    )

    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    return {
        "id": new_org.id,
        "nama": new_org.nama,
        "keterangan": new_org.keterangan
    }
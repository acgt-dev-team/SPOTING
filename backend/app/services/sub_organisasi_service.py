from sqlalchemy.orm import Session
from app.models.sub_organisasi import SubOrganisasi


def get_sub_by_organisasi(db: Session, organisasi_id: int):
    subs = db.query(SubOrganisasi).filter(
        SubOrganisasi.organisasi_id == organisasi_id
    ).all()

    return [
        {
            "id": s.id,
            "nama": s.nama,
            "keterangan": s.keterangan,
            "kod": s.kod,
            "aktif": s.aktif
        }
        for s in subs
    ]


def create_sub_organisasi(db: Session, data: dict):
    new_sub = SubOrganisasi(
        organisasi_id=data["organisasi_id"],
        kod=data["kod"],
        nama=data["nama"],
        keterangan=data.get("keterangan", "")
    )

    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)

    return {
        "id": new_sub.id,
        "nama": new_sub.nama,
        "keterangan": new_sub.keterangan
    }
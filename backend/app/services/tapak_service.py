from sqlalchemy.orm import Session
from app.models.tapak import Tapak


def get_tapak_by_sub(db: Session, sub_id: int):
    try:
        print("👉 FETCHING tapak for sub_id:", sub_id)

        tapaks = db.query(Tapak).filter(
            Tapak.sub_organisasi_id == sub_id
        ).all()

        print("👉 RAW RESULT:", tapaks)

        result = [
            {
                "id": t.id,
                "nama": t.nama,
                "keterangan": t.keterangan,  # ✅ FIXED
                "kod": t.kod,
                "aktif": t.aktif
            }
            for t in tapaks
        ]

        print("👉 FINAL RESULT:", result)

        return result

    except Exception as e:
        print("🔥 SERVICE ERROR:", str(e))
        raise e


def create_tapak(db: Session, data: dict):
    try:
        new_tapak = Tapak(
            sub_organisasi_id=data["sub_organisasi_id"],
            kod=data["kod"],
            nama=data["nama"],
            keterangan=data.get("keterangan", "")  # ✅ FIXED
        )

        db.add(new_tapak)
        db.commit()
        db.refresh(new_tapak)

        return {
            "id": new_tapak.id,
            "nama": new_tapak.nama,
            "keterangan": new_tapak.keterangan
        }

    except Exception as e:
        print("🔥 CREATE ERROR:", str(e))
        raise e
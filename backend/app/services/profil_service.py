from sqlalchemy.orm import Session
from app.models.profil import Profil
import re
from sqlalchemy import func
from app.models.x_profil_tugasan import XProfilTugasan

def get_profil_by_tapak(db: Session, tapak_id: int):
    profils = (
        db.query(
            Profil,
            func.count(
                func.distinct(XProfilTugasan.tugasan_id)
            ).label("tugasan_count")
        )
        .outerjoin(
            XProfilTugasan,
            XProfilTugasan.profil_id == Profil.id
        )
        .filter(
            Profil.tapak_id == tapak_id
        )
        .group_by(Profil.id)
        .all()
    )

    response = []

    for profil, tugasan_count in profils:

        # get all task statuses under this profile
        tasks = db.query(XProfilTugasan).filter(
            XProfilTugasan.profil_id == profil.id
        ).all()

        statuses = [task.status_id for task in tasks]

        # determine profile execution status
        if 2 in statuses:
            execution_status = "Dalam Proses"

        elif len(statuses) > 0 and all(status == 3 for status in statuses):
            execution_status = "Telah Selesai"

        else:
            execution_status = "Belum Bermula"

        response.append({
            "id": profil.id,
            "tapak_id": profil.tapak_id,
            "nama": profil.nama,
            "keterangan": profil.keterangan,
            "kod": profil.kod,
            "aktif": bool(profil.aktif) if profil.aktif is not None else False,
            "execution_type": profil.execution_type,
            "cron_expression": profil.cron_expression,
            "is_scheduled": profil.is_scheduled,
            "tugasan_count": tugasan_count,
            "execution_status": execution_status
        })

    return response


#create

def generate_next_profil_kod(db: Session):
    latest_profile = (
        db.query(Profil)
        .filter(Profil.kod.like("PRF%"))
        .order_by(Profil.id.desc())
        .first()
    )

    if not latest_profile:
        return "PRF001"

    match = re.search(r"PRF(\d+)", latest_profile.kod)

    if not match:
        return "PRF001"

    next_number = int(match.group(1)) + 1

    return f"PRF{next_number:03d}"

def create_profil(db: Session, data: dict):
    new_profil = Profil(
        tapak_id=data["tapak_id"],
        kod=generate_next_profil_kod(db),
        nama=data["nama"],
        keterangan=data.get("keterangan", ""),
        execution_type=data.get("execution_type", "IMMEDIATE"),
        cron_expression=data.get("cron_expression"),
        is_scheduled=data.get("is_scheduled", False),
        report_template=data.get("report_template", "DEFAULT"),
        report_format=data.get("report_format", "EXCEL")
    )

    db.add(new_profil)
    db.commit()
    db.refresh(new_profil)

    return {
    "id": new_profil.id,
    "tapak_id": new_profil.tapak_id,
    "kod": new_profil.kod,
    "nama": new_profil.nama,
    "keterangan": new_profil.keterangan,
    "aktif": bool(new_profil.aktif) if new_profil.aktif is not None else False,
    "execution_type": new_profil.execution_type,
    "cron_expression": new_profil.cron_expression,
    "is_scheduled": new_profil.is_scheduled,
    "report_template": new_profil.report_template,
    "report_format": new_profil.report_format
}

# =========================
# UPDATE
# =========================
def update_profil(db: Session, id: int, data: dict):
    profil = db.query(Profil).filter(Profil.id == id).first()

    if not profil:
        return None

    profil.nama = data["nama"]
    profil.keterangan = data.get("keterangan", "")
    profil.execution_type = data.get("execution_type", "IMMEDIATE")
    profil.cron_expression = data.get("cron_expression")
    profil.is_scheduled = data.get("is_scheduled", False)
    profil.report_template = data.get("report_template", "DEFAULT")
    profil.report_format = data.get("report_format", "EXCEL")


    db.commit()
    db.refresh(profil)

    return {
        "id": profil.id,
        "tapak_id": profil.tapak_id,
        "kod": profil.kod,
        "nama": profil.nama,
        "keterangan": profil.keterangan,
        "aktif": bool(profil.aktif) if profil.aktif is not None else False,
        "execution_type": profil.execution_type,
        "cron_expression": profil.cron_expression,
        "is_scheduled": profil.is_scheduled,
        "report_template": profil.report_template,
        "report_format": profil.report_format
    }


# =========================
# DELETE
# =========================
def delete_profil(db: Session, id: int):
    profil = db.query(Profil).filter(Profil.id == id).first()

    if not profil:
        return False

    db.delete(profil)
    db.commit()
    return True
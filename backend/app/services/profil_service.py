from sqlalchemy.orm import Session
from app.models.profil import Profil
import re
from sqlalchemy import func
from app.models.x_profil_tugasan import XProfilTugasan

# =========================
# GET
# =========================
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

        response.append({
            "id": profil.id,
            "tapak_id": profil.tapak_id,
            "nama": profil.nama,
            "keterangan": profil.keterangan,
            "kod": profil.kod,
            "aktif": bool(profil.aktif) if profil.aktif is not None else False,
            "execution_type": profil.execution_type,
            "scheduled_at": profil.scheduled_at,
            "is_scheduled": profil.is_scheduled,
            "tugasan_count": tugasan_count,
            "execution_status": profil.execution_status   # ✅ source of truth
        })

    return response


# =========================
# GENERATE KOD
# =========================
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


# =========================
# CREATE
# =========================
def create_profil(db: Session, data: dict):

    execution_type = data.get("execution_type", "IMMEDIATE")

    # ✅ status logic
    if execution_type == "IMMEDIATE":
        status = "in process"
    else:
        status = "telah dijadualkan"

    new_profil = Profil(
        tapak_id=data["tapak_id"],
        kod=generate_next_profil_kod(db),
        nama=data["nama"],
        keterangan=data.get("keterangan", ""),
        execution_type=execution_type,
        scheduled_at=data.get("scheduled_at"),
        is_scheduled=(execution_type == "SCHEDULED"),
        execution_status=status,
        report_template=data.get("report_template", "DEFAULT"),
        report_format=data.get("report_format", "EXCEL")
    )

    db.add(new_profil)
    db.commit()
    db.refresh(new_profil)

    # ✅ IMMEDIATE execution trigger
    if execution_type == "IMMEDIATE":
        from app.scheduler.profile_scheduler import run_single_profile
        run_single_profile(new_profil.id)

    return {
        "id": new_profil.id,
        "tapak_id": new_profil.tapak_id,
        "kod": new_profil.kod,
        "nama": new_profil.nama,
        "keterangan": new_profil.keterangan,
        "aktif": bool(new_profil.aktif) if new_profil.aktif is not None else False,
        "execution_type": new_profil.execution_type,
        "scheduled_at": new_profil.scheduled_at,
        "is_scheduled": new_profil.is_scheduled,
        "execution_status": new_profil.execution_status,
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
    profil.scheduled_at = data.get("scheduled_at")
    profil.is_scheduled = (profil.execution_type == "SCHEDULED")

    # ✅ update status
    if profil.execution_type == "IMMEDIATE":
        profil.execution_status = "in process"
    else:
        profil.execution_status = "telah dijadualkan"

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
        "scheduled_at": profil.scheduled_at,
        "is_scheduled": profil.is_scheduled,
        "execution_status": profil.execution_status,
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
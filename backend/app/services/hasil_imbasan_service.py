from sqlalchemy.orm import Session

from app.models.hasil_imbasan import HasilImbasan
from app.schemas.hasil_imbasan import HasilImbasanCreate
from datetime import datetime

from app.models.profil import Profil
from app.models.x_profil_tugasan import XProfilTugasan

def create_hasil_imbasan(
    db: Session,
    request: HasilImbasanCreate
):
    hasil = HasilImbasan(
        profil_tugasan_id=request.profil_tugasan_id,
        ejen_id=request.ejen_id,
        machine_id=request.machine_id,
        hasil=request.hasil
    )

    db.add(hasil)
    db.commit()
    db.refresh(hasil)

    assignment = (
        db.query(XProfilTugasan)
        .filter(
            XProfilTugasan.id == request.profil_tugasan_id
        )
        .first()
    )

    if not assignment:
        return hasil

    assignment.status_id = 3
    assignment.selesai_pada = datetime.now()

    db.commit()

    total_tasks = (
        db.query(XProfilTugasan)
        .filter(
            XProfilTugasan.profil_id == assignment.profil_id
        )
        .count()
    )

    remaining = (
        db.query(XProfilTugasan)
        .filter(
            XProfilTugasan.profil_id == assignment.profil_id,
            XProfilTugasan.status_id != 3
        )
        .count()
    )

    if total_tasks > 0 and remaining == 0:

        profile = (
            db.query(Profil)
            .filter(
                Profil.id == assignment.profil_id
            )
            .first()
        )

        if profile:
            profile.execution_status = "execution completed"
            db.commit()

    return hasil

def mark_task_failed(
    db: Session,
    profil_tugasan_id: int
):

    assignment = (
        db.query(XProfilTugasan)
        .filter(
            XProfilTugasan.id == profil_tugasan_id
        )
        .first()
    )

    if not assignment:
        return {"status": "not found"}

    assignment.status_id = 4
    assignment.selesai_pada = datetime.now()

    db.commit()

    profile = (
        db.query(Profil)
        .filter(
            Profil.id == assignment.profil_id
        )
        .first()
    )

    if profile:
        profile.execution_status = "gagal"
        db.commit()

    return {"status": "failed"}
from sqlalchemy.orm import Session

from app.models.ejen import Ejen
from app.models.profil import Profil
from app.models.x_profil_tugasan import XProfilTugasan
from app.models.tugasan import Tugasan
from datetime import datetime

def get_tasks_for_agent(
    db: Session,
    ejen_id: int
):
    ejen = db.query(Ejen).filter(
        Ejen.id == ejen_id
    ).first()

    if not ejen:
        return []

    # Heartbeat
    ejen.last_seen = datetime.now()
    ejen.status = "Running"
    db.commit()

    profiles = db.query(Profil).filter(
        Profil.tapak_id == ejen.tapak_id,
        Profil.execution_status == "in process"
    ).all()

    results = []

    for profile in profiles:

        assignments = (
            db.query(XProfilTugasan)
            .filter(
                XProfilTugasan.profil_id == profile.id,
                XProfilTugasan.status_id == 1
            )
            .all()
        )

        for assignment in assignments:

            task = db.query(Tugasan).filter(
                Tugasan.id == assignment.tugasan_id
            ).first()

            if not task:
                continue

            results.append({

                "profil_tugasan_id": assignment.id,

                "profil_id": profile.id,
                "profil_nama": profile.nama,

                "tugasan_id": task.id,
                "nama": task.nama,
                "kod": task.kod,

                "protocol": task.protocol,
                "ip_start": task.ip_start,
                "ip_end": task.ip_end

            })

    return results

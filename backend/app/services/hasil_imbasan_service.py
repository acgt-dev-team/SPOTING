from datetime import datetime

from sqlalchemy.orm import Session

from app.models.hasil_imbasan import HasilImbasan
from app.models.profil import Profil
from app.models.x_profil_ejen import XProfilEjen
from app.models.x_profil_tugasan import XProfilTugasan
from app.models.x_profil_tugasan_ejen import XProfilTugasanEjen
from app.schemas.hasil_imbasan import HasilImbasanCreate


def create_hasil_imbasan(
    db: Session,
    request: HasilImbasanCreate
):
    # ------------------------------------------
    # Load Task-Agent assignment
    # ------------------------------------------
    task_agent = (
        db.query(XProfilTugasanEjen)
        .filter(
            XProfilTugasanEjen.id ==
            request.profil_tugasan_ejen_id
        )
        .first()
    )

    if not task_agent:
        raise Exception(
            "Task-Agent assignment not found."
        )

    profil_task = task_agent.task_assignment

    # ------------------------------------------
    # Save scan result
    # ------------------------------------------
    hasil = HasilImbasan(
        profil_tugasan_id=profil_task.id,
        ejen_id=request.ejen_id,
        machine_id=request.machine_id,
        hasil=request.hasil
    )

    db.add(hasil)

    # ------------------------------------------
    # Complete this Task-Agent
    # ------------------------------------------
    task_agent.status = "Completed"
    task_agent.completed_at = datetime.now()

    db.commit()
    db.refresh(hasil)
    
    # ------------------------------------------
    # Has EVERY agent completed THIS task?
    # ------------------------------------------
    remaining_task_agents = (
        db.query(XProfilTugasanEjen)
        .filter(
            XProfilTugasanEjen.profil_tugasan_id == profil_task.id,
            XProfilTugasanEjen.status != "Completed"
        )
        .count()
    )

    if remaining_task_agents == 0:

        # Status 3 = Completed
        profil_task.status_id = 3

        profil_task.selesai_pada = datetime.now()

    db.commit()
    db.refresh(hasil)

    # ------------------------------------------
    # Has this agent completed every task
    # in this profile?
    # ------------------------------------------
    remaining_agent_tasks = (
        db.query(XProfilTugasanEjen)
        .join(
            XProfilTugasan,
            XProfilTugasan.id ==
            XProfilTugasanEjen.profil_tugasan_id
        )
        .filter(
            XProfilTugasan.profil_id ==
            profil_task.profil_id,

            XProfilTugasanEjen.ejen_id ==
            request.ejen_id,

            XProfilTugasanEjen.status !=
            "Completed"
        )
        .count()
    )

    if remaining_agent_tasks == 0:

        profile_agent = (
            db.query(XProfilEjen)
            .filter(
                XProfilEjen.profil_id ==
                profil_task.profil_id,

                XProfilEjen.ejen_id ==
                request.ejen_id
            )
            .first()
        )

        if profile_agent:

            profile_agent.status = "Completed"
            profile_agent.completed_at = datetime.now()

    # ------------------------------------------
    # Have ALL agents completed ALL tasks?
    # ------------------------------------------
    remaining = (
        db.query(XProfilTugasanEjen)
        .join(
            XProfilTugasan,
            XProfilTugasan.id ==
            XProfilTugasanEjen.profil_tugasan_id
        )
        .filter(
            XProfilTugasan.profil_id ==
            profil_task.profil_id,

            XProfilTugasanEjen.status !=
            "Completed"
        )
        .count()
    )

    if remaining == 0:

        profile = (
            db.query(Profil)
            .filter(
                Profil.id ==
                profil_task.profil_id
            )
            .first()
        )

        if profile:
            profile.execution_status = (
                "execution completed"
            )
            profile.kemaskini_pada = datetime.now()

    db.commit()

    return hasil

def mark_task_failed(
    db: Session,
    profil_tugasan_ejen_id: int
):

    task_agent = (
        db.query(XProfilTugasanEjen)
        .filter(
            XProfilTugasanEjen.id ==
            profil_tugasan_ejen_id
        )
        .first()
    )

    if not task_agent:
        return {
            "status": "not found"
        }

    task_agent.status = "Failed"
    task_agent.completed_at = datetime.now()

    profile = task_agent.task_assignment.profile

    if profile:
        profile.execution_status = "gagal"

    db.commit()

    return {
        "status": "failed"
    }

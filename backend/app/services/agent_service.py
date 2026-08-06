from datetime import datetime

from sqlalchemy.orm import Session

from app.models.ejen import Ejen
from app.models.x_profil_ejen import XProfilEjen
from app.models.x_profil_tugasan_ejen import XProfilTugasanEjen


def get_tasks_for_agent(
    db: Session,
    ejen_id: int
):
    ejen = (
        db.query(Ejen)
        .filter(Ejen.id == ejen_id)
        .first()
    )

    if not ejen:
        return []

    # ------------------------------------------
    # Heartbeat
    # ------------------------------------------
    ejen.last_seen = datetime.now()
    ejen.status = "Running"
    db.commit()

    # ------------------------------------------
    # Profiles assigned to this agent
    # ------------------------------------------
    assignments = (
        db.query(XProfilEjen)
        .filter(
            XProfilEjen.ejen_id == ejen.id,
            XProfilEjen.status.in_(["Pending", "Running"])
        )
        .all()
    )

    results = []

    for assignment in assignments:

        profile = assignment.profile

        # ------------------------------------------
        # Agent starts this profile
        # ------------------------------------------
        if assignment.status == "Pending":

            assignment.status = "Running"

            if assignment.started_at is None:
                assignment.started_at = datetime.now()

            db.commit()

        # ------------------------------------------
        # Ignore inactive profiles
        # ------------------------------------------
        if profile.execution_status != "in process":
            continue

        # ------------------------------------------
        # Pending tasks for THIS profile and THIS agent
        # ------------------------------------------
        agent_tasks = (
            db.query(XProfilTugasanEjen)
            .join(XProfilTugasanEjen.task_assignment)
            .filter(
                XProfilTugasanEjen.ejen_id == ejen.id,
                XProfilTugasanEjen.status == "Pending",
                XProfilTugasanEjen.task_assignment.has(
                    profil_id=profile.id
                )
            )
            .all()
        )

        for task_assignment in agent_tasks:

            # ------------------------------------------
            # Mark task as Running
            # ------------------------------------------
            task_assignment.status = "Running"

            if task_assignment.started_at is None:
                task_assignment.started_at = datetime.now()

            # ------------------------------------------
            # Mark Profile-Task as Running
            # (only the first time)
            # ------------------------------------------
            profil_task = task_assignment.task_assignment

            if profil_task.jadualkan_pada is None:
                profil_task.jadualkan_pada = datetime.now()

            # Status 2 = Running / In Process
            if profil_task.status_id == 1:
                profil_task.status_id = 2

            db.commit()

            profil_task = task_assignment.task_assignment
            task = profil_task.tugasan

            if not task:
                continue

            results.append({

                # keep this for Phase 4.5
                "profil_tugasan_ejen_id": task_assignment.id,

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

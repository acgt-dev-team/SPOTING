from sqlalchemy.orm import Session

from app.models.x_profil_ejen import XProfilEjen
from app.models.x_profil_tugasan import XProfilTugasan
from app.models.x_profil_tugasan_ejen import XProfilTugasanEjen


def create_task_agent_assignments(
    db: Session,
    profil_id: int
):
    """
    Create Task-Agent assignments for every task
    belonging to a profile.

    Safe to call multiple times.
    """

    tasks = (
        db.query(XProfilTugasan)
        .filter(
            XProfilTugasan.profil_id == profil_id
        )
        .all()
    )

    if not tasks:
        return

    agents = (
        db.query(XProfilEjen)
        .filter(
            XProfilEjen.profil_id == profil_id
        )
        .all()
    )

    created = 0

    for task in tasks:

        for agent in agents:

            exists = (
                db.query(XProfilTugasanEjen)
                .filter(
                    XProfilTugasanEjen.profil_tugasan_id == task.id,
                    XProfilTugasanEjen.ejen_id == agent.ejen_id
                )
                .first()
            )

            if exists:
                continue

            db.add(
                XProfilTugasanEjen(
                    profil_tugasan_id=task.id,
                    ejen_id=agent.ejen_id,
                    status="Pending"
                )
            )

            created += 1

    db.commit()

    print(f"[Task-Agent] Created {created} task assignments.")

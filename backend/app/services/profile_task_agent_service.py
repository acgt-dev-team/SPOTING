from sqlalchemy.orm import Session

from app.models.x_profil_ejen import XProfilEjen
from app.models.x_profil_tugasan import XProfilTugasan
from app.models.x_profil_tugasan_ejen import XProfilTugasanEjen


def create_task_agent_assignments(
    db: Session,
    profil_tugasan_id: int
):
    """
    Create Task-Agent assignments for one profile task.

    Every assigned agent will receive this task.
    """

    profil_task = (
        db.query(XProfilTugasan)
        .filter(
            XProfilTugasan.id == profil_tugasan_id
        )
        .first()
    )

    if not profil_task:
        return

    agents = (
        db.query(XProfilEjen)
        .filter(
            XProfilEjen.profil_id == profil_task.profil_id
        )
        .all()
    )

    created = 0

    for agent in agents:

        exists = (
            db.query(XProfilTugasanEjen)
            .filter(
                XProfilTugasanEjen.profil_tugasan_id == profil_task.id,
                XProfilTugasanEjen.ejen_id == agent.ejen_id
            )
            .first()
        )

        if exists:
            continue

        db.add(
            XProfilTugasanEjen(
                profil_tugasan_id=profil_task.id,
                ejen_id=agent.ejen_id,
                status="Pending"
            )
        )

        created += 1

    db.commit()

    print(
        f"[Task-Agent] Created {created} task assignments."
    )

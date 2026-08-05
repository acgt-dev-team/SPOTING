from sqlalchemy.orm import Session

from app.models.ejen import Ejen
from app.models.x_profil_ejen import XProfilEjen

from app.services.profile_task_agent_service import (
    create_task_agent_assignments
)


def assign_agents_to_profile(
    db: Session,
    profile_id: int,
):
    """
    Assign every registered agent to a profile.

    This function is idempotent:
    existing assignments are preserved,
    only missing assignments are created.

    After assigning agents, create the corresponding
    Task-Agent assignments.
    """

    agents = db.query(Ejen).all()

    created = 0

    for agent in agents:

        exists = (
            db.query(XProfilEjen)
            .filter(
                XProfilEjen.profil_id == profile_id,
                XProfilEjen.ejen_id == agent.id,
            )
            .first()
        )

        if exists:
            continue

        db.add(
            XProfilEjen(
                profil_id=profile_id,
                ejen_id=agent.id,
                status="Pending",
            )
        )

        created += 1

    db.commit()

    print(
        f"[Profile-Agent] Created {created} agent assignments."
    )

    # ------------------------------------------
    # Create Task-Agent assignments
    # ------------------------------------------
    create_task_agent_assignments(
        db,
        profile_id
    )

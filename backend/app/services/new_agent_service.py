from sqlalchemy.orm import Session
from datetime import datetime

from app.models.profil import Profil
from app.models.ejen import Ejen
from app.models.x_profil_ejen import XProfilEjen
from app.models.x_profil_tugasan import XProfilTugasan
from app.models.x_profil_tugasan_ejen import XProfilTugasanEjen


def attach_new_agent_to_profile(
    db: Session,
    agent: Ejen
):
    """
    Called immediately after a NEW agent is registered.

    This function:

    1. Creates the Profile-Agent assignment.
    2. Creates Task-Agent assignments for every task
       in the agent's profile.
    3. If the profile was already completed,
       revive it so only this new agent executes.
    """

    # ------------------------------------------
    # Load profile
    # ------------------------------------------
    profile = (
        db.query(Profil)
        .filter(
            Profil.id == agent.profile_id
        )
        .first()
    )

    if not profile:
        return

    # ------------------------------------------
    # Create Profile-Agent assignment
    # ------------------------------------------
    profile_agent = (
        db.query(XProfilEjen)
        .filter(
            XProfilEjen.profil_id == profile.id,
            XProfilEjen.ejen_id == agent.id
        )
        .first()
    )

    if profile_agent is None:

        profile_agent = XProfilEjen(
            profil_id=profile.id,
            ejen_id=agent.id,
            status="Pending"
        )

        db.add(profile_agent)

    # ------------------------------------------
    # Create Task-Agent assignments
    # ------------------------------------------
    profile_tasks = (
        db.query(XProfilTugasan)
        .filter(
            XProfilTugasan.profil_id == profile.id
        )
        .all()
    )

    created = 0

    for profile_task in profile_tasks:

        exists = (
            db.query(XProfilTugasanEjen)
            .filter(
                XProfilTugasanEjen.profil_tugasan_id == profile_task.id,
                XProfilTugasanEjen.ejen_id == agent.id
            )
            .first()
        )

        if exists:
            continue

        db.add(
            XProfilTugasanEjen(
                profil_tugasan_id=profile_task.id,
                ejen_id=agent.id,
                status="Pending"
            )
        )

        created += 1

    # ------------------------------------------
    # Revive completed profile
    # ------------------------------------------
    if profile.execution_status == "execution completed":

        profile.execution_status = "in process"
        profile.kemaskini_pada = datetime.now()

    db.commit()

    print(
        f"[New Agent] Agent {agent.id} attached to Profile {profile.id}"
    )

    print(
        f"[New Agent] Created {created} Task-Agent assignments."
    )
    
    return agent

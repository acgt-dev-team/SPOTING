from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.ejen import Ejen
from app.models.profil import Profil
from app.services.new_agent_service import (
    attach_new_agent_to_profile
)

def register_ejen(
    db: Session,
    ip_address: str,
    tapak_id: int,
    machine_id: UUID,
    hostname: str,
    profile_id: int,
):
    """
    Register an agent.

    Identity is based on machine_id.

    Existing machine:
        - update IP
        - update hostname
        - update tapak
        - refresh heartbeat
        - keep existing profile assignment

    New machine:
        - create a new agent using the supplied profile.
    """

    machine_uuid = UUID(str(machine_id))

    # ----------------------------------------------------
    # Existing agent
    # ----------------------------------------------------
    ejen = (
        db.query(Ejen)
        .filter(Ejen.machine_id == machine_uuid)
        .first()
    )

    if ejen:
        ejen.ip_address = ip_address
        ejen.hostname = hostname
        ejen.tapak_id = tapak_id

        # Heartbeat
        ejen.status = "Running"
        ejen.last_seen = datetime.now()

        db.commit()
        db.refresh(ejen)

        return ejen

    # ----------------------------------------------------
    # Verify profile exists
    # ----------------------------------------------------
    profile = (
        db.query(Profil)
        .filter(Profil.id == profile_id)
        .first()
    )

    if profile is None:
        raise Exception(
            f"Profile {profile_id} does not exist."
        )

    # ----------------------------------------------------
    # Create new agent
    # ----------------------------------------------------
    ejen = Ejen(
        ip_address=ip_address,
        tapak_id=tapak_id,
        machine_id=machine_uuid,
        hostname=hostname,
        profile_id=profile.id,
        status="Running",
        last_seen=datetime.now(),
    )

    db.add(ejen)
    db.commit()
    db.refresh(ejen)
    
    attach_new_agent_to_profile(
        db=db,
        agent=ejen
    )
    
    return ejen

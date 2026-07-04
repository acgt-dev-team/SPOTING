from sqlalchemy.orm import Session

from app.models.ejen import Ejen


def register_ejen(
    db: Session,
    ip_address: str,
    tapak_id: int
):
    """
    Register an agent.

    If the IP already exists:
        - update its tapak if needed
        - return existing agent

    Otherwise create a new one.
    """

    ejen = (
        db.query(Ejen)
        .filter(Ejen.ip_address == ip_address)
        .first()
    )

    if ejen:

        if ejen.tapak_id != tapak_id:
            ejen.tapak_id = tapak_id
            db.commit()
            db.refresh(ejen)

        return ejen

    ejen = Ejen(
        ip_address=ip_address,
        tapak_id=tapak_id
    )

    db.add(ejen)
    db.commit()
    db.refresh(ejen)

    return ejen
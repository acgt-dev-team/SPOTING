from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models.ejen import Ejen


def heartbeat(
    db: Session,
    ejen_id: int,
):
    """
    Update an agent heartbeat.

    Every polling request refreshes the agent's
    last_seen timestamp and marks it Running.
    """

    ejen = (
        db.query(Ejen)
        .filter(Ejen.id == ejen_id)
        .first()
    )

    if ejen is None:
        return

    ejen.last_seen = func.now()
    ejen.status = "Running"

    db.commit()

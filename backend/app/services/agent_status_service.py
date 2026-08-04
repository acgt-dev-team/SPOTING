from datetime import datetime, timedelta, timezone

from app.models.ejen import Ejen


OFFLINE_TIMEOUT_SECONDS = 60


def update_agent_status(db):
    """
    Mark agents Offline if they have not
    checked in recently.
    """

    cutoff = datetime.now(timezone.utc) - timedelta(
        seconds=OFFLINE_TIMEOUT_SECONDS
    )

    agents = db.query(Ejen).all()

    changed = False

    for agent in agents:

        if agent.last_seen is None:
            continue

        last_seen = agent.last_seen

        # PostgreSQL TIMESTAMP WITHOUT TIME ZONE
        if last_seen.tzinfo is None:
            last_seen = last_seen.replace(
                tzinfo=timezone.utc
            )

        if last_seen < cutoff:

            if agent.status != "Offline":
                print(
                    f"[Agent] {agent.hostname} -> Offline"
                )

                agent.status = "Offline"
                changed = True

        else:

            if agent.status != "Running":
                print(
                    f"[Agent] {agent.hostname} -> Running"
                )

                agent.status = "Running"
                changed = True

    if changed:
        db.commit()

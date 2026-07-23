import uuid
from pathlib import Path

# Store the Machine ID in the user's home directory
MACHINE_ID_FILE = Path.home() / ".cbom_machine_id"


def get_machine_id():
    """
    Returns a persistent Machine ID.
    Generates one if it doesn't exist yet.
    """

    if MACHINE_ID_FILE.exists():
        return MACHINE_ID_FILE.read_text().strip()

    machine_id = str(uuid.uuid4())

    MACHINE_ID_FILE.write_text(machine_id)

    return machine_id
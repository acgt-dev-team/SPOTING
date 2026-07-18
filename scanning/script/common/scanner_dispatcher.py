from BinariesUsed_agct import run_scan as run_binaries_used


SCANNERS = {
    "BIN_USED": run_binaries_used,
}


def execute_task(task):
    """
    Execute the scanner for a backend task.

    Returns:
        dict: JSON scan result
    """

    code = task["kod"]

    if code not in SCANNERS:
        raise Exception(f"Unsupported task code: {code}")

    return SCANNERS[code]()
from BinariesUsed_agct import run_scan as run_binaries_used
from Libraries_agct import run_scan as run_libraries
from BinariesDisk_agct import run_scan as run_binaries_disk

SCANNERS = {
    "BIN_USED": run_binaries_used,
    "BIN_DISK": run_binaries_disk,
    "LIBRARIES": run_libraries
}


def execute_task(task):
    """
    Execute the scanner for a backend task.

    Returns:
        dict: JSON scan result
    """

    code = task["kod"]

    print("Task code received:", repr(code))
    print("Supported scanners:", SCANNERS.keys())

    if code not in SCANNERS:
        raise Exception(f"Unsupported task code: {code}")

    return SCANNERS[code]()
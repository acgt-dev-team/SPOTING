from BinariesUsed_agct import run_scan as run_binaries_used
from Libraries_agct import run_scan as run_libraries
from BinariesDisk_agct import run_scan as run_binaries_disk
from CertKeys_agct import run_scan as run_cert_keys
from ExeCodes_agct import run_scan as run_execodes
from Kernel_mod_agct import run_scan as run_kernel_modules
from NetworkProtocol_agct import run_scan as run_network_protocol
from NetworkApp_agct import run_scan as run_network_app

SCANNERS = {
    "BIN_USED": run_binaries_used,
    "BIN_DISK": run_binaries_disk,
    "LIBRARIES": run_libraries,
    "CERT_KEYS": run_cert_keys,
    "EXEC_SCRIPT": run_execodes,
    "KERNEL_MODULES": run_kernel_modules,
    "NETWORK_PROTOCOL": run_network_protocol,
    "NETWORK_APP": run_network_app,
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
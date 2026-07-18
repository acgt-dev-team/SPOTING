import os
import platform

# ==========================================================
# OS DETECTION
# ==========================================================

def detect_os():
    if os.name == "nt" or platform.system().lower().startswith("win"):
        return "windows"
    return "unix"


OS_TYPE = detect_os()

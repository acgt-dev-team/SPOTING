import os
import psutil

from common.os_utils import OS_TYPE


def list_running_binaries():
    binaries = set()

    if OS_TYPE == "unix":
        proc_dir = "/proc"

        for pid in os.listdir(proc_dir):
            if not pid.isdigit():
                continue

            exe_path = os.path.join(proc_dir, pid, "exe")

            try:
                real_exe = os.readlink(exe_path)

                if os.path.isfile(real_exe) and os.access(real_exe, os.X_OK):
                    binaries.add(real_exe)

            except Exception:
                continue

    else:  # Windows
        for proc in psutil.process_iter(["exe"]):
            try:
                exe = proc.info["exe"]

                if exe and os.path.isfile(exe):
                    binaries.add(exe)

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                continue

    print(len(binaries), " detected")
    return sorted(binaries)
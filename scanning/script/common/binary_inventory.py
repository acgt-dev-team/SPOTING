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


def is_executable(path):
    """
    Returns True if the file is considered an executable
    for the current operating system.
    """
    if OS_TYPE == "windows":
        return (
            os.path.isfile(path)
            and path.lower().endswith(".exe")
        )

    return (
        os.path.isfile(path)
        and os.access(path, os.X_OK)
    )


def list_disk_binaries():
    """
    Returns executables found in directories listed in PATH.
    """

    binaries = set()

    for directory in os.environ.get("PATH", "").split(os.pathsep):

        if not os.path.isdir(directory):
            continue

        try:
            for filename in os.listdir(directory):

                full_path = os.path.join(directory, filename)

                if is_executable(full_path):
                    binaries.add(full_path)

        except Exception:
            continue

    print(len(binaries), "detected")

    return sorted(binaries)



import os

from common.os_utils import OS_TYPE


if OS_TYPE == "unix":
    LIB_DIRS = [
        "/lib",
        "/lib64",
        "/usr/lib",
        "/usr/lib64",
        "/usr/local/lib",
    ]
    LIB_EXTS = (".so", ".a", ".la")

else:

    LIB_DIRS = [
        os.path.join(
            os.environ.get("SystemRoot", "C:\\Windows"),
            "System32",
        ),
        os.path.join(
            os.environ.get("SystemRoot", "C:\\Windows"),
            "SysWOW64",
        ),
    ]

    LIB_EXTS = (".dll", ".lib")


def is_library(path):

    if OS_TYPE == "windows":
        return path.lower().endswith(LIB_EXTS)

    return (
        path.endswith(LIB_EXTS)
        or ".so." in path
    )


def list_libraries():

    libraries = set()

    for directory in LIB_DIRS:

        if not os.path.isdir(directory):
            continue

        for root, _, files in os.walk(directory):

            for filename in files:

                full_path = os.path.join(root, filename)

                if is_library(full_path):
                    libraries.add(os.path.realpath(full_path))

    print(len(libraries), "libraries detected")

    return sorted(libraries)
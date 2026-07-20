import os
import psutil

from common.os_utils import OS_TYPE
import subprocess
from pathlib import Path




CERT_EXTENSIONS = {
    ".crt",
    ".cer",
    ".pem",
    ".der",
    ".key",
    ".pk8",
    ".p12",
    ".pfx",
}

SCRIPT_EXTENSIONS = {
    ".py",
    ".sh",
    ".pl",
    ".rb",
    ".ps1",
    ".bat",
    ".cmd",
}

WEB_EXTENSIONS = {
    ".php",
    ".py",
    ".js",
    ".ts",
    ".java",
    ".go",
    ".rb",
    ".jsp",
    ".cs",
    ".scala",
}


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





def list_certificate_files(scan_root=None):

    if scan_root is None:

        if OS_TYPE == "windows":
            scan_root = "C:\\"

        else:
            scan_root = "/"

    files = []

    for root, _, filenames in os.walk(scan_root):

        for filename in filenames:

            if os.path.splitext(filename)[1].lower() in CERT_EXTENSIONS:

                files.append(
                    os.path.join(root, filename)
                )

    print(len(files), "certificate/key files detected")

    return sorted(files)


def list_script_files():
    """
    Returns script files from common script locations.
    """

    files = set()

    if OS_TYPE == "windows":

        search_dirs = []

        # PATH directories
        search_dirs.extend(
            d for d in os.environ.get("PATH", "").split(os.pathsep)
            if os.path.isdir(d)
        )

        # User profile
        user_profile = os.environ.get("USERPROFILE")
        if user_profile:
            search_dirs.append(user_profile)

    else:

        search_dirs = [
            "/usr/bin",
            "/usr/local/bin",
            "/opt",
            os.path.expanduser("~"),
        ]

    for directory in search_dirs:

        try:
            for root, _, filenames in os.walk(directory):

                for filename in filenames:

                    ext = os.path.splitext(filename)[1].lower()

                    if ext in SCRIPT_EXTENSIONS:

                        files.add(
                            os.path.join(root, filename)
                        )

        except Exception:
            continue

    print(f"{len(files)} script files detected")

    return sorted(files)


def list_kernel_modules():
    """
    Return kernel modules.
    Linux:
        *.ko
    Windows:
        *.sys
    """

    if OS_TYPE == "linux":

        try:

            kernel_ver = (
                Path("/proc/sys/kernel/osrelease")
                .read_text()
                .strip()
            )

            base = f"/lib/modules/{kernel_ver}"

            modules = subprocess.check_output(
                [
                    "find",
                    base,
                    "-type",
                    "f",
                    "-name",
                    "*.ko*",
                ],
                text=True,
            ).splitlines()

            print(f"{len(modules)} kernel modules detected")

            return sorted(modules)

        except Exception:

            return []

    # Windows
    modules = []

    windows_driver_dir = os.path.join(
        os.environ.get("SystemRoot", "C:\\Windows"),
        "System32",
        "drivers",
    )

    if os.path.isdir(windows_driver_dir):

        for root, _, files in os.walk(windows_driver_dir):

            for filename in files:

                if filename.lower().endswith(".sys"):

                    modules.append(
                        os.path.join(root, filename)
                    )

    print(f"{len(modules)} kernel drivers detected")

    return sorted(modules)


def list_tls_targets():
    """
    Returns listening TLS targets.
    """

    targets = []

    TLS_PORTS = {
        443,
        465,
        563,
        636,
        853,
        989,
        990,
        992,
        993,
        995,
        8443,
    }

    for conn in psutil.net_connections(kind="inet"):

        if conn.status != psutil.CONN_LISTEN:
            continue

        port = conn.laddr.port

        if port not in TLS_PORTS:
            continue

        ip = conn.laddr.ip

        targets.append(f"{ip}:{port}")

    print(f"{len(targets)} TLS targets detected")

    return sorted(set(targets))

def list_web_files():
    """
    Returns web application source files from common web roots.
    """

    files = set()

    if OS_TYPE == "windows":

        search_dirs = [
            r"C:\inetpub\wwwroot",
            r"C:\xampp\htdocs",
            r"C:\wamp64\www",
        ]

    else:

        search_dirs = [
            "/var/www",
            "/usr/share/nginx",
            "/srv/www",
        ]

    for directory in search_dirs:

        if not os.path.isdir(directory):
            continue

        try:
            for root, dirs, filenames in os.walk(directory):

                for filename in filenames:

                    ext = os.path.splitext(filename)[1].lower()

                    if ext in WEB_EXTENSIONS:
                        files.add(os.path.join(root, filename))

        except Exception:
            continue

    print(f"{len(files)} web files detected")

    return sorted(files)
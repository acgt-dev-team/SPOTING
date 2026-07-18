import os
import subprocess

from common.crypto_rules import CRYPTO_LIB_PATTERNS


# ==========================================================
# COMMAND EXECUTION
# ==========================================================

def run_cmd(cmd):
    """
    Execute a Linux command and return its output.
    """

    try:
        if isinstance(cmd, list):
            return subprocess.check_output(
                cmd,
                stderr=subprocess.DEVNULL,
                timeout=15
            ).decode(errors="ignore")

        return subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.DEVNULL,
            timeout=15
        ).decode(errors="ignore")

    except Exception:
        return ""


# ==========================================================
# ELF HELPERS
# ==========================================================

def run_ldd(binary_path):
    """
    Return ldd output.
    """
    return run_cmd(["ldd", binary_path])


def run_nm(binary_path):
    """
    Return exported/imported dynamic symbols.
    """
    return run_cmd(["nm", "-D", binary_path])


def run_objdump(binary_path):
    """
    Return objdump output.
    """
    return run_cmd(["objdump", "-x", binary_path])


def run_readelf(binary_path):
    """
    Return readelf output.
    """
    return run_cmd(["readelf", "-a", binary_path])


def run_strings(binary_path):
    """
    Return printable strings from a binary.
    """
    return run_cmd(["strings", binary_path])


# ==========================================================
# LIBRARY CLASSIFICATION
# ==========================================================

def classify_libraries(binary_path):
    """
    Split libraries into system and third-party libraries.
    """

    if not os.path.exists(binary_path):
        return [], []

    output = run_ldd(binary_path)

    if not output:
        return [], []

    system_libs = []
    third_party_libs = []

    system_paths = [
        "/lib",
        "/lib64",
        "/usr/lib",
        "/usr/lib64",
    ]

    for line in output.splitlines():

        if "=>" not in line:
            continue

        parts = line.split("=>", 1)

        if len(parts) < 2:
            continue

        lib_path = parts[1].split("(")[0].strip()

        if not lib_path or lib_path == "not found":
            continue

        if any(lib_path.startswith(path) for path in system_paths):
            system_libs.append(lib_path)
        else:
            third_party_libs.append(lib_path)

    return third_party_libs, system_libs


# ==========================================================
# CRYPTO LIBRARIES
# ==========================================================

def get_crypto_deps(binary_path):
    """
    Return detected crypto libraries linked by an ELF binary.
    """

    output = run_ldd(binary_path)

    deps = []

    for line in output.splitlines():
        for lib in CRYPTO_LIB_PATTERNS:
            if lib.lower() in line.lower():
                deps.append(lib)

    deps = sorted(set(deps))

    return ",".join(deps) if deps else "none"
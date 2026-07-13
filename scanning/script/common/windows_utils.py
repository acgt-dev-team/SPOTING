import glob
import os
import shutil
import subprocess
import re
from common.os_utils import OS_TYPE


# ==========================================================
# DUMPBIN DISCOVERY
# ==========================================================

def find_dumpbin():
    """
    Automatically locate dumpbin.exe.
    """

    dumpbin = shutil.which("dumpbin")
    if dumpbin:
        return dumpbin

    search_roots = [
        r"C:\Program Files (x86)\Microsoft Visual Studio",
        r"C:\Program Files\Microsoft Visual Studio",
    ]

    for root in search_roots:
        pattern = os.path.join(root, "**", "dumpbin.exe")
        matches = glob.glob(pattern, recursive=True)

        if matches:
            matches.sort(reverse=True)
            return matches[0]

    return None


DUMPBIN_PATH = (
    find_dumpbin()
    if OS_TYPE == "windows"
    else None
)


# ==========================================================
# COMMAND EXECUTION
# ==========================================================

def run_cmd(cmd):
    """
    Execute a command and return its output.
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
            stderr=subprocess.DEVNULL,
            shell=True,
            timeout=15
        ).decode(errors="ignore")

    except Exception:
        return ""


def run_dumpbin(arguments):
    """
    Execute dumpbin with the supplied arguments.
    Example:
        run_dumpbin('/imports "abc.exe"')
    """

    if OS_TYPE != "windows":
        return ""

    if not DUMPBIN_PATH:
        return ""

    return run_cmd(f'"{DUMPBIN_PATH}" {arguments}')


def run_strings(binary_path):
    """
    Return printable strings from a PE binary.
    """

    return run_cmd(f'strings "{binary_path}"')

# ==========================================================
# PE HELPERS
# ==========================================================

def get_pe_imports(binary_path):
    """
    Return dumpbin /imports output.
    """

    return run_dumpbin(f'/imports "{binary_path}"')





def get_imported_functions(binary_path):
    """
    Return every imported API/function from dumpbin /imports.
    """

    output = get_pe_imports(binary_path)

    functions = []

    pattern = re.compile(
        r"^\s*[0-9A-F]+\s+([A-Za-z_][A-Za-z0-9_]*)$",
        re.IGNORECASE
    )

    for line in output.splitlines():

        match = pattern.match(line)

        if match:
            functions.append(match.group(1))

    return functions

def get_pe_dependents(binary_path):
    """
    Return dumpbin /dependents output.
    """

    return run_dumpbin(f'/dependents "{binary_path}"')


def get_pe_exports(binary_path):
    """
    Return dumpbin /exports output.
    """

    return run_dumpbin(f'/exports "{binary_path}"')


def get_pe_symbols(binary_path):
    """
    Return dumpbin /symbols output.
    """

    return run_dumpbin(f'/symbols "{binary_path}"')


def get_version_info(binary_path):
    """
    Placeholder for future implementation.
    """

    return {}


def get_signer(binary_path):
    """
    Placeholder for future Authenticode implementation.
    """

    return None


# ==========================================================
# LIBRARY CLASSIFICATION
# ==========================================================

def classify_libraries(binary_path):
    """
    Split imported DLLs into third-party and Windows system libraries.
    """

    if OS_TYPE != "windows":
        return [], []

    if not os.path.exists(binary_path):
        return [], []

    output = get_pe_dependents(binary_path)

    if not output:
        return [], []

    system_libs = []
    third_party_libs = []

    windows_system = [
        "kernel32.dll",
        "user32.dll",
        "advapi32.dll",
        "gdi32.dll",
        "shell32.dll",
        "ole32.dll",
        "ws2_32.dll",
        "ntdll.dll",
        "ucrtbase.dll",
        "vcruntime",
    ]

    for line in output.splitlines():

        line = line.strip()

        if not line.lower().endswith(".dll"):
            continue

        if any(x in line.lower() for x in windows_system):
            system_libs.append(line)
        else:
            third_party_libs.append(line)

    return third_party_libs, system_libs


# ==========================================================
# CRYPTO LIBRARIES
# ==========================================================

from common.crypto_rules import CRYPTO_LIB_PATTERNS


def get_crypto_deps(binary_path):
    """
    Return detected crypto libraries imported by the PE.
    """

    if OS_TYPE != "windows":
        return "none"

    output = get_pe_imports(binary_path)

    deps = []

    for line in output.splitlines():
        for lib in CRYPTO_LIB_PATTERNS:
            if lib.lower() in line.lower():
                deps.append(lib)

    deps = sorted(set(deps))

    return ",".join(deps) if deps else "none"
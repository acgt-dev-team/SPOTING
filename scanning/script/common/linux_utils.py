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
    Return nm output.
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
    Return printable strings from an ELF binary.
    """
    return run_cmd(["strings", binary_path])
# ==========================================================
# IMPORTED FUNCTIONS
# ==========================================================

def get_imported_functions(binary_path):
    """
    Return imported functions from an ELF binary.
    Uses the dynamic symbol table.
    """

    output = run_cmd(["readelf", "--dyn-syms", binary_path])

    functions = []

    for line in output.splitlines():

        line = line.strip()

        if "FUNC" not in line:
            continue

        parts = line.split()

        if len(parts) < 8:
            continue

        symbol = parts[-1]

        # Remove version suffixes
        # e.g. printf@GLIBC_2.2.5 -> printf
        symbol = symbol.split("@")[0]

        if symbol:
            functions.append(symbol)

    return sorted(set(functions))


# ==========================================================
# ELF DEPENDENCIES
# ==========================================================

def get_elf_dependents(binary_path):
    """
    Return all shared libraries required by the ELF.
    """

    output = run_ldd(binary_path)

    libraries = []

    for line in output.splitlines():

        if "=>" not in line:
            continue

        lib = line.split("=>")[0].strip()

        if lib:
            libraries.append(lib)

    return sorted(set(libraries))


# ==========================================================
# EXPORTED FUNCTIONS
# ==========================================================

def get_elf_exports(binary_path):
    """
    Return exported function names.
    """

    output = run_nm(binary_path)

    exports = []

    for line in output.splitlines():

        parts = line.split()

        if len(parts) < 3:
            continue

        symbol_type = parts[1]

        if symbol_type.upper() not in ("T", "W"):
            continue

        exports.append(parts[2])

    return sorted(set(exports))


# ==========================================================
# SYMBOL TABLE
# ==========================================================

def get_elf_symbols(binary_path):
    """
    Return raw symbol table output.
    """

    return run_nm(binary_path)
# ==========================================================
# LIBRARY CLASSIFICATION
# ==========================================================

def classify_libraries(binary_path):
    """
    Split linked shared libraries into third-party and system libraries.
    """

    if not os.path.exists(binary_path):
        return [], []

    output = run_ldd(binary_path)

    if not output:
        return [], []

    system_libs = []
    third_party_libs = []

    system_paths = (
        "/lib",
        "/lib64",
        "/usr/lib",
        "/usr/lib64",
        "/usr/lib/x86_64-linux-gnu",
        "/lib/x86_64-linux-gnu",
    )

    for line in output.splitlines():

        if "=>" not in line:
            continue

        parts = line.split("=>", 1)

        if len(parts) < 2:
            continue

        lib_path = parts[1].split("(")[0].strip()

        if not lib_path or lib_path == "not found":
            continue

        if lib_path.startswith(system_paths):
            system_libs.append(lib_path)
        else:
            third_party_libs.append(lib_path)

    return (
        sorted(set(third_party_libs)),
        sorted(set(system_libs))
    )


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

        line_lower = line.lower()

        for lib in CRYPTO_LIB_PATTERNS:

            if lib.lower() in line_lower:
                deps.append(lib)

    deps = sorted(set(deps))

    return ",".join(deps) if deps else "none"


# ==========================================================
# PLACEHOLDERS (API compatibility)
# ==========================================================

def get_version_info(binary_path):
    """
    Placeholder for future ELF version information.
    """
    return {}


def get_signer(binary_path):
    """
    Linux ELF binaries are typically unsigned.
    """
    return None

# ==========================================================
# COMPATIBILITY WRAPPERS
# (Windows API equivalents)
# ==========================================================

def get_pe_imports(binary_path):
    """
    Windows compatibility wrapper.
    On Linux this returns the dynamic symbol table.
    """
    return run_cmd(["readelf", "--dyn-syms", binary_path])


def get_pe_dependents(binary_path):
    """
    Windows compatibility wrapper.
    On Linux this returns ldd output.
    """
    return run_ldd(binary_path)


def get_pe_exports(binary_path):
    """
    Windows compatibility wrapper.
    On Linux this returns exported symbols.
    """
    return run_nm(binary_path)


def get_pe_symbols(binary_path):
    """
    Windows compatibility wrapper.
    On Linux this returns the symbol table.
    """
    return run_nm(binary_path)


# ==========================================================
# PUBLIC API
# ==========================================================

__all__ = [
    "run_cmd",
    "run_ldd",
    "run_nm",
    "run_objdump",
    "run_readelf",
    "run_strings",
    "get_imported_functions",
    "get_elf_dependents",
    "get_elf_exports",
    "get_elf_symbols",
    "classify_libraries",
    "get_crypto_deps",
    "get_version_info",
    "get_signer",
    "get_pe_imports",
    "get_pe_dependents",
    "get_pe_exports",
    "get_pe_symbols",
]

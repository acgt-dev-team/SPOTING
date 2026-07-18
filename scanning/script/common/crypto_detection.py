import re

from common.crypto_rules import CRYPTO_LIB_PATTERNS, CRYPTO_RULES
from common.libraries import CRYPTO_API_RULES
from common.crypto_api_detection import detect_crypto_apis

from common.os_utils import OS_TYPE

from common.windows_utils import (
    DUMPBIN_PATH,
    get_pe_imports,
    get_pe_symbols,
    run_cmd,
)

from common.linux_utils import (
    run_ldd,
    run_nm,
)

# ==========================================================
# CRYPTO DETECTION
# ==========================================================

def detect_crypto(binary):
    results = detect_crypto_apis(binary)

    if OS_TYPE == "unix":
        strings_out = run_cmd(["strings", binary]).lower()
        symbols_out = run_nm(binary).lower()
        deps_out = run_ldd(binary).lower()

    else:
        if not DUMPBIN_PATH:
            return []

        strings_out = run_cmd(f'strings "{binary}"').lower()
        symbols_out = get_pe_symbols(binary).lower()
        deps_out = get_pe_imports(binary).lower()

    # --------------------------------------------------
    # Group detected APIs   
    # --------------------------------------------------

    grouped = {}

    for hit in results:

        key = (
            hit["primitive"],
            hit["algorithm"]
        )

        if key not in grouped:

            grouped[key] = {
                "algorithm": hit["algorithm"],
                "primitive": hit["primitive"],
                "apis": [],
                "confidence": hit["confidence"],
                "detection_source": set(hit["detection_source"]),
            }

            if hit.get("deprecated"):
                grouped[key]["deprecated"] = True

        grouped[key]["apis"].append(hit["api"])

    for entry in grouped.values():

        entry["apis"].sort()

        count = len(entry["apis"])

        if count >= 5:
            entry["confidence"] = "very_high"
        elif count >= 2:
            entry["confidence"] = "high"
        else:
            entry["confidence"] = "medium"

    results = list(grouped.values())

    # --------------------------------------------------
    # Existing string/signature detection
    # --------------------------------------------------

    for name, meta in CRYPTO_RULES.items():
        algo = meta.get("algorithmProperties", {})
        proto = meta.get("protocolProperties", {})

        pattern = rf"\b{re.escape(name.lower())}\b"

        if (
            not re.search(pattern, strings_out)
            and not re.search(pattern, symbols_out)
        ):
            continue

        entry = {
            "algorithm": algo.get("algorithm", name),
            "primitive": algo.get(
                "primitive",
                proto.get("protocolType", "unknown"),
            ),
            "parameters": {},
            "confidence": "low",
            "detection_source": set(),
        }

        # --------------------------------------------------
        # Key Length
        # --------------------------------------------------
        for size in algo.get("keyLengths", []):
            if str(size) in strings_out:
                entry["parameters"]["keyLength"] = size
                entry["confidence"] = "medium"
                entry["detection_source"].add("string")
                break

        # --------------------------------------------------
        # Cipher Mode
        # --------------------------------------------------
        for mode in algo.get("modes", []):
            if mode.lower() in strings_out:
                entry["parameters"]["mode"] = mode
                entry["detection_source"].add("string")
                break

        # --------------------------------------------------
        # ECC Curve
        # --------------------------------------------------
        for curve in algo.get("curves", []):
            if curve.lower() in strings_out:
                entry["parameters"]["curve"] = curve
                entry["confidence"] = "medium"
                entry["detection_source"].add("string")
                break

        # --------------------------------------------------
        # Hash Function
        # --------------------------------------------------
        for h in algo.get("hashFunctions", []):
            if h.lower() in strings_out:
                entry["parameters"]["hash"] = h
                entry["detection_source"].add("string")
                break

        # --------------------------------------------------
        # Protocol Version
        # --------------------------------------------------
        for v in proto.get("versions", []):
            if v in strings_out:
                entry["parameters"]["version"] = v
                entry["detection_source"].add("string")
                break

        # --------------------------------------------------
        # Crypto library detection
        # --------------------------------------------------
        if any(lib in deps_out for lib in CRYPTO_LIB_PATTERNS):
            entry["detection_source"].add("crypto-library")
            entry["confidence"] = "medium"

        # --------------------------------------------------
        # Deprecated algorithms
        # --------------------------------------------------
        if algo.get("deprecated"):
            entry["deprecated"] = True

        already_detected = False

        for existing in results:
            if existing["algorithm"] == entry["algorithm"]:
                existing["detection_source"].update(
                    entry["detection_source"]
                )
                already_detected = True
                break

        if not already_detected:
            results.append(entry)

    return results
#!/usr/bin/env python3

import os
import csv
import psutil

from common.binary_inventory import list_running_binaries
from common.binary_metadata import guess_language
from common.crypto_detection import detect_crypto

from common.platform_utils import (
    classify_libraries,
    get_crypto_deps,
)

# ==========================================================
# BINARY STATE
# ==========================================================

def check_binary_state(file_path):
    """
    Differentiates the state of a binary:
    In Use, In Transit, or At Rest.
    """
    if not os.path.exists(file_path):
        return "File does not exist on disk."

    abs_path = os.path.abspath(file_path)

    # ------------------------------------------------------
    # IN USE
    # ------------------------------------------------------
    for proc in psutil.process_iter(["exe", "name"]):
        try:
            if proc.info["exe"] and os.path.abspath(proc.info["exe"]) == abs_path:
                return f"STATE: IN USE (Running as PID {proc.pid})"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # ------------------------------------------------------
    # IN TRANSIT
    # ------------------------------------------------------
    transit_tools = [
        "wget",
        "scp",
        "rsync",
        "curl",
        "sftp-server",
        "transmission",
    ]

    for proc in psutil.process_iter(["name", "open_files"]):
        try:
            if proc.info["name"] in transit_tools:
                files = proc.open_files()
                if files:
                    for f in files:
                        if os.path.abspath(f.path) == abs_path:
                            return (
                                f"STATE: IN TRANSIT "
                                f"(Being moved by {proc.info['name']})"
                            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # ------------------------------------------------------
    # AT REST
    # ------------------------------------------------------
    return "STATE: AT REST (Static on disk)"


# ==========================================================
# MAIN
# ==========================================================

def main():
    with open("binaries_used.csv", "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "resource",
            "resource_type",
            "category",
            "item",
            "property",
            "value",
            "evidence",
            "confidence",
            "severity"
        ])

        for binary in list_running_binaries():
            print(f"\nProcessing: {binary}", flush=True)
            print(binary)

            language = guess_language(binary)
            print("[OK] Language", flush=True)

            third_party, system = classify_libraries(binary)
            print("[OK] Libraries", flush=True)

            libs = get_crypto_deps(binary)
            print("[OK] Crypto deps", flush=True)

            if libs == "none":
                continue

            hits = detect_crypto(binary)
            merged = {}

            for hit in hits:

                key = (
                    hit["algorithm"],
                    hit["primitive"]
                )

                if key not in merged:

                    merged[key] = hit.copy()

                    merged[key]["apis"] = []

                if "api" in hit:
                    merged[key]["apis"].append(hit["api"])

                merged[key]["detection_source"] = (
                    merged[key]["detection_source"]
                    |
                    hit["detection_source"]
                )

                confidence_rank = {
                    "low": 1,
                    "medium": 2,
                    "high": 3,
                    "very_high": 4,
                }

                if confidence_rank.get(hit.get("confidence", "low"), 0) > confidence_rank.get(
                    merged[key].get("confidence", "low"), 0
                ):
                    merged[key]["confidence"] = hit["confidence"]

            hits = list(merged.values())
            print("[OK] Crypto detection", flush=True)

            if not hits:
                writer.writerow([
                    binary,
                    os.path.splitext(binary)[1].lstrip("."),
                    "binary",
                    "crypto-library",
                    "dependency",
                    libs,
                    "import table",
                    "",
                    "info"
                ])
                continue

            for hit in hits:

                # Skip generic wrapper APIs (e.g. OpenSSL EVP)
                if hit["primitive"] == "multiple":
                    continue

                params = hit.get("parameters", {})
                key_len = params.pop("keyLength", "unknown")

                if key_len != "unknown":
                    property_name = "key_length"
                    value = key_len
                else:
                    property_name = "detected"
                    if hit.get("apis"):

                        value = ",".join(sorted(hit["apis"]))

                    else:

                        value = "yes"

                severity = "warning" if hit.get("deprecated") else "info"

                writer.writerow([
                    binary,
                    os.path.splitext(binary)[1].lstrip("."),
                    hit["primitive"],
                    hit["algorithm"],
                    property_name,
                    value,
                    ",".join(sorted(hit["detection_source"])),
                    hit.get("confidence", ""),
                    severity
                ])


def display():
    for binary in list_running_binaries():
        language = guess_language(binary)
        third_party, system = classify_libraries(binary)
        libs = get_crypto_deps(binary)
        state = check_binary_state(binary)

        if libs == "none":
            continue

        print("Binary :", binary)
        print("Language :", language)
        print("State :", state)

        print("System Library :", system)
        for syslib in system:
            print(syslib)
            hits = detect_crypto(syslib)
            print(hits)

        print("Third Party Library :", third_party)
        print("Crypto Library :", libs)

        hits = detect_crypto(binary)
        merged = {}

        for hit in hits:

            key = (
                hit["algorithm"],
                hit["primitive"]
            )

            if key not in merged:

                merged[key] = hit.copy()

                merged[key]["apis"] = []

            if "api" in hit:
                merged[key]["apis"].append(hit["api"])

            merged[key]["detection_source"] = (
                merged[key]["detection_source"]
                |
                hit["detection_source"]
            )

        hits = list(merged.values())
        for hit in hits:
            print(hit)


if __name__ == "__main__":
    main()
    # display()

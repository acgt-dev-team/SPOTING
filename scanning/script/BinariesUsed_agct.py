#!/usr/bin/env python3

import os
import psutil

from common.binary_inventory import list_running_binaries
from common.binary_metadata import guess_language
from common.crypto_detection import detect_crypto
from common.binary_profile import BinaryProfile
from common.csv_exporter import export_csv
from common.json_exporter import export_json
from common.confidence import calculate_overall_confidence

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
    profiles = []
    for binary in list_running_binaries():
        print(f"\nProcessing: {binary}", flush=True)
        print(binary)

        profile = BinaryProfile(
            path=binary,
            filename=os.path.basename(binary),
            extension=os.path.splitext(binary)[1].lstrip("."),
        )

        language = guess_language(binary)
        profile.language = language
        print("[OK] Language", flush=True)

        third_party, system = classify_libraries(binary)
        profile.third_party_libraries = third_party
        profile.system_libraries = system
        print("[OK] Libraries", flush=True)

        libs = get_crypto_deps(binary)
        if libs != "none":
            profile.crypto_dependencies = libs.split(",")
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
        profile.detections = hits
        profile.overall_confidence = calculate_overall_confidence(profile)
        print("[OK] Crypto detection", flush=True)
        profiles.append(profile)
        
    export_csv(profiles)

    json_result = export_json(profiles)

    return json_result

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

def run_scan():
    """
    Entry point used by the AGCT agent.
    Returns the scan result as a Python dictionary.
    """
    return main()

if __name__ == "__main__":
    main()
    # display()

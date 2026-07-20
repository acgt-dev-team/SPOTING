#!/usr/bin/env python3

import os
import psutil

from common.binary_inventory import list_libraries
from common.binary_metadata import guess_language
from common.crypto_detection import detect_crypto
from common.binary_profile import BinaryProfile
from common.json_exporter import export_json
from common.confidence import calculate_overall_confidence

from common.platform_utils import get_crypto_deps

def main():
    profiles = []

    libraries = list_libraries()

    total = len(libraries)

    for index, binary in enumerate(libraries, start=1):

        print(
            f"\n[{index}/{total}] Processing: {binary}",
            flush=True
        )

        profile = BinaryProfile(
            path=binary,
            filename=os.path.basename(binary),
            extension=os.path.splitext(binary)[1].lstrip("."),
        )

        language = guess_language(binary)
        profile.language = language
        print("[OK] Language", flush=True)

        profile.third_party_libraries = []
        profile.system_libraries = []

        print("[OK] Library")


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

    json_result = export_json( profiles)

    return json_result



def run_scan():
    """
    Entry point used by the AGCT agent.
    Returns the scan result as a Python dictionary.
    """
    return main()

if __name__ == "__main__":
    main()
    # display()

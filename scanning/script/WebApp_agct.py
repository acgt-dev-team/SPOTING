#!/usr/bin/env python3

import os

from common.binary_inventory import list_web_files
from common.script_utils import scan_file

from common.binary_profile import BinaryProfile
from common.confidence import calculate_overall_confidence

from common.csv_exporter import export_csv
from common.json_exporter import export_json


def main():

    profiles = []

    files = list_web_files()

    total = len(files)

    print(f"Scanning {total} web files...")

    for index, path in enumerate(files, start=1):

        print(f"[{index}/{total}] {path}")

        try:

            hits = scan_file(path)

            if not hits:
                continue

            profile = BinaryProfile(
                path=path,
                filename=os.path.basename(path),
                extension=os.path.splitext(path)[1].lstrip("."),
            )

            profile.detections = hits

            profile.overall_confidence = calculate_overall_confidence(profile)

            profiles.append(profile)

        except Exception as e:
            print(f"Failed to scan {path}: {e}")

    export_csv(
        profiles,
        output_file="web_app.csv",
    )

    json_result = export_json(
        profiles,
        output_file="web_app.json",
    )

    return json_result


def run_scan():
    return main()


if __name__ == "__main__":
    main()
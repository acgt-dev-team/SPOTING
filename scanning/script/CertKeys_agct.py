#!/usr/bin/env python3

import os

from common.binary_inventory import list_certificate_files
from common.certificate_utils import analyze_file

from common.binary_profile import BinaryProfile
from common.csv_exporter import export_csv
from common.json_exporter import export_json


def main():

    profiles = []

    files = list_certificate_files()

    total = len(files)

    for index, cert_file in enumerate(files, start=1):

        print(
            f"\n[{index}/{total}] Processing: {cert_file}",
            flush=True,
        )

        result = analyze_file(cert_file)

        if result is None:
            continue

        profile = BinaryProfile(
            path=cert_file,
            filename=os.path.basename(cert_file),
            extension=os.path.splitext(cert_file)[1].lstrip("."),
        )

        profile.detections = [result]

        profiles.append(profile)

    export_csv(
        profiles,
        output_file="cert_keys.csv",
    )

    json_result = export_json(
        profiles,
        output_file="cert_keys.json",
    )

    return json_result

def run_scan():
    return main()


if __name__ == "__main__":
    main()

    